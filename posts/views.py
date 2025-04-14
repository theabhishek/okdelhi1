from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Subreddit
from .forms import PostCreateForm, CommentCreateForm
from subreddits.models import Subreddit
from django.utils.text import slugify

@login_required
def post_create(request, subreddit_slug=None):
    subreddit = None
    if subreddit_slug:
        subreddit = get_object_or_404(Subreddit, slug=subreddit_slug)
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        
        if subreddit:
            form.data = form.data.copy()
            form.data['subreddit'] = subreddit.id
        
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.author = request.user
                
                # Generate a unique slug from the title
                base_slug = slugify(post.title)
                unique_slug = base_slug
                counter = 1
                while Post.objects.filter(slug=unique_slug).exists():
                    unique_slug = f"{base_slug}-{counter}"
                    counter += 1
                post.slug = unique_slug
                
                # Save the post first
                post.save()
                
                # Handle the image upload for image posts
                if post.post_type == 'image' and 'image' in request.FILES:
                    post.image = request.FILES['image']
                    post.save(update_fields=['image'])
                
                # Handle URL for link posts
                if post.post_type == 'link' and 'url' in form.cleaned_data:
                    post.url = form.cleaned_data['url']
                    post.save(update_fields=['url'])
                
                # Handle content for text posts
                if post.post_type == 'text' and 'content' in form.cleaned_data:
                    post.content = form.cleaned_data['content']
                    post.save(update_fields=['content'])
                
                messages.success(request, 'Post created successfully!')
                return redirect('posts:detail', subreddit_slug=post.subreddit.slug, post_slug=post.slug)
            except Exception as e:
                messages.error(request, f'Error creating post: {str(e)}')
                print(f"Error creating post: {str(e)}")  # For debugging
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    print(f"Form error - {field}: {error}")  # For debugging
    else:
        initial = {}
        if subreddit:
            initial['subreddit'] = subreddit
        form = PostCreateForm(initial=initial)
        
        if subreddit:
            form.fields['subreddit'].widget.attrs['readonly'] = True
            form.fields['subreddit'].widget.attrs['class'] = 'bg-gray-100'
    
    context = {
        'form': form,
        'subreddit': subreddit,
    }
    return render(request, 'posts/create.html', context)

def post_detail(request, subreddit_slug, post_slug):
    post = get_object_or_404(Post, slug=post_slug, subreddit__slug=subreddit_slug)
    comments = post.comments.filter(parent=None)
    comment_form = CommentCreateForm()
    return render(request, 'posts/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def post_edit(request, subreddit_slug, post_slug):
    post = get_object_or_404(Post, slug=post_slug, subreddit__slug=subreddit_slug)
    if request.user != post.author:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('posts:detail', subreddit_slug=subreddit_slug, post_slug=post_slug)
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('posts:detail', subreddit_slug=subreddit_slug, post_slug=post_slug)
    else:
        form = PostCreateForm(instance=post)
    return render(request, 'posts/edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, subreddit_slug, post_slug):
    post = get_object_or_404(Post, slug=post_slug, subreddit__slug=subreddit_slug)
    if request.user != post.author and request.user not in post.subreddit.moderators.all():
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('posts:detail', subreddit_slug=subreddit_slug, post_slug=post_slug)
    
    subreddit_slug = post.subreddit.slug
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('subreddits:detail', slug=subreddit_slug)

@login_required
def post_upvote(request, subreddit_slug, post_slug):
    post = get_object_or_404(Post, slug=post_slug, subreddit__slug=subreddit_slug)
    if request.user in post.downvotes.all():
        post.downvotes.remove(request.user)
    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)
    else:
        post.upvotes.add(request.user)
    post.update_score()
    next_url = request.GET.get('next', 'posts:detail')
    if next_url == 'home':
        return redirect('home')
    return redirect('posts:detail', subreddit_slug=subreddit_slug, post_slug=post_slug)

@login_required
def post_downvote(request, subreddit_slug, post_slug):
    post = get_object_or_404(Post, slug=post_slug, subreddit__slug=subreddit_slug)
    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)
    if request.user in post.downvotes.all():
        post.downvotes.remove(request.user)
    else:
        post.downvotes.add(request.user)
    post.update_score()
    next_url = request.GET.get('next', 'posts:detail')
    if next_url == 'home':
        return redirect('home')
    return redirect('posts:detail', subreddit_slug=subreddit_slug, post_slug=post_slug)

@login_required
def comment_create(request, subreddit_slug, post_slug):
    post = get_object_or_404(Post, slug=post_slug, subreddit__slug=subreddit_slug)
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
    return redirect('posts:detail', subreddit_slug=subreddit_slug, post_slug=post_slug)

@login_required
def comment_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = parent_comment.post
            comment.parent = parent_comment
            comment.save()
            messages.success(request, 'Reply added successfully!')
    return redirect('posts:detail', subreddit_slug=parent_comment.post.subreddit.slug, post_slug=parent_comment.post.slug)

@login_required
def comment_upvote(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.downvotes.all():
        comment.downvotes.remove(request.user)
    if request.user in comment.upvotes.all():
        comment.upvotes.remove(request.user)
    else:
        comment.upvotes.add(request.user)
    comment.update_score()
    return redirect('posts:detail', subreddit_slug=comment.post.subreddit.slug, post_slug=comment.post.slug)

@login_required
def comment_downvote(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.upvotes.all():
        comment.upvotes.remove(request.user)
    if request.user in comment.downvotes.all():
        comment.downvotes.remove(request.user)
    else:
        comment.downvotes.add(request.user)
    comment.update_score()
    return redirect('posts:detail', subreddit_slug=comment.post.subreddit.slug, post_slug=comment.post.slug) 