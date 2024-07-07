from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'vote_app2'  # Đặt tên namespace cho ứng dụng

urlpatterns = [
    path('register/', views.register, name='register'),
    path('otp_verification/<int:user_id>/', views.otp_verification, name='otp_verification'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),

]