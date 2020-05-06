from django.urls import path

from . import views

app_name = 'register'
urlpatterns = [
    path('', views.create_account, name='create_account'),
    path('profile/', views.profile_page, name='profile_page'),
    path('profile/<name_user>/', views.profile_image, name='profile_image'),
]