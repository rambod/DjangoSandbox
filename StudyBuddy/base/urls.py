from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = "login"),
    path('register/',views.registerPage, name = "register"),
    path('logout/', views.logoutUser, name = "logout"),
    path('', views.home, name = "home"),
    path('profile/<int:pk>', views.userPofile, name = "user-profile"),
    path('room/<int:pk>/', views.room, name = "room"),
    path('create-room/', views.createRoom, name = "create-room"),
    path('update-room/<int:pk>/', views.updateRoom, name = "update-room"),
    path('delete-room/<int:pk>/', views.deleteRoom, name = "delete-room"),
    path('delete-message/<int:pk>/', views.deleteMessage, name = "delete-message"),
    path('update-message/<int:pk>/', views.updateMessage, name = "update-message"),
]