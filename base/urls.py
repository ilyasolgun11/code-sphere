from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('room-creation/', views.create_room, name='create-room'),
    path('room-update/<str:pk>/', views.update_room, name='update-room'),
    path('room-deletion/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
]