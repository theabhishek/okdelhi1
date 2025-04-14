from django.urls import path
from . import views

app_name = 'lost_and_found'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('create/', views.create_item, name='create_item'),
    path('my-items/', views.my_items, name='my_items'),
    path('admin/approval/', views.admin_approval, name='admin_approval'),
    path('admin/approve/<int:pk>/', views.approve_item, name='approve_item'),
    path('admin/reject/<int:pk>/', views.reject_item, name='reject_item'),
    path('mark-resolved/<int:pk>/', views.mark_resolved, name='mark_resolved'),
] 