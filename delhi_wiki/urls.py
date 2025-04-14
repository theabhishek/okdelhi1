from django.urls import path
from . import views

app_name = 'delhi_wiki'

urlpatterns = [
    # Area URLs
    path('areas/', views.area_list, name='area_list'),
    path('areas/create/', views.area_create, name='area_create'),
    path('areas/approve/', views.area_approval_list, name='area_approval_list'),
    path('areas/<slug:slug>/approve/', views.approve_area, name='approve_area'),
    path('areas/<slug:slug>/', views.area_detail, name='area_detail'),

    # Landmark URLs
    path('landmarks/', views.landmark_list, name='landmark_list'),
    path('landmarks/create/', views.landmark_create, name='landmark_create'),
    path('landmarks/approve/', views.landmark_approval_list, name='landmark_approval_list'),
    path('landmarks/<slug:slug>/approve/', views.approve_landmark, name='approve_landmark'),
    path('landmarks/<slug:slug>/', views.landmark_detail, name='landmark_detail'),
    path('landmarks/<slug:slug>/review/', views.landmark_review_create, name='landmark_review_create'),

    # Food Place URLs
    path('food-places/', views.food_place_list, name='food_place_list'),
    path('food-places/create/', views.food_place_create, name='food_place_create'),
    path('food-places/approve/', views.food_place_approval_list, name='food_place_approval_list'),
    path('food-places/<slug:slug>/approve/', views.approve_food_place, name='approve_food_place'),
    path('food-places/<slug:slug>/', views.food_place_detail, name='food_place_detail'),
    path('food-places/<slug:slug>/review/', views.food_place_review_create, name='food_place_review_create'),

    # Market URLs
    path('markets/', views.market_list, name='market_list'),
    path('markets/create/', views.market_create, name='market_create'),
    path('markets/approve/', views.market_approval_list, name='market_approval_list'),
    path('markets/<slug:slug>/approve/', views.approve_market, name='approve_market'),
    path('markets/<slug:slug>/', views.market_detail, name='market_detail'),
    path('markets/<slug:slug>/review/', views.market_review_create, name='market_review_create'),

    # Event URLs
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/approve/', views.event_approval_list, name='event_approval_list'),
    path('events/<slug:slug>/approve/', views.approve_event, name='approve_event'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('events/<slug:slug>/review/', views.event_review_create, name='event_review_create'),
    path('search/', views.search, name='search'),
] 