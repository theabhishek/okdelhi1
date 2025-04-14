from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('users/', include('users.urls', namespace='users')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('subreddits/', include('subreddits.urls', namespace='subreddits')),
    path('pg-rental/', include('pg_rental.urls', namespace='pg_rental')),
    path('delhi-wiki/', include('delhi_wiki.urls', namespace='delhi_wiki')),
    path('bus/', include('bus_service.urls', namespace='bus_service')),
    path('coupons/', include('coupon_service.urls', namespace='coupon_service')),
    path('metro/', include('metro.urls', namespace='metro')),
    path('medical/', include('medical.urls', namespace='medical')),
    path('hotel/', include('hotel_service.urls', namespace='hotel_service')),
    path('jobs/', include('job_portal.urls', namespace='job_portal')),
    path('lost-and-found/', include('lost_and_found.urls', namespace='lost_and_found')),
    path('storytelling/', include('storytelling.urls', namespace='storytelling')),
    path('news/', include('news.urls', namespace='news')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 