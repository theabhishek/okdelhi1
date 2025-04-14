from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='my_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
] 