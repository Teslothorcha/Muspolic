from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'register'
urlpatterns = [
    path('', views.create_account, name='create_account'),
    path('profile/', views.profile_page, name='profile_page'),
    path('profile/<name_user>/', views.profile_image, name='profile_image'),
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
        name='password_reset'),
    path('password-reset/done', 
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
]