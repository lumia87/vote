from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'vote_app2'  # Đặt tên namespace cho ứng dụng

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register, name='register'),
    path('otp_verification/<int:user_id>/', views.otp_verification, name='otp_verification'),
    path('login/', views.login_view, name='login'),
    path('assign/', views.assign_contestants_to_user, name='assign_contestants'),
    path('view_all_scores/', views.view_all_scores, name='view_all_scores'),
    path('contestant_home/', views.contestant_home, name='contestant_home'),

]