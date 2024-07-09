from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'vote_app2'  # Đặt tên namespace cho ứng dụng

urlpatterns = [
    path('register/', views.register, name='register'),
    path('otp_verification/<int:user_id>/', views.otp_verification, name='otp_verification'),
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='home'),
    path('contestants/', views.contestant_list, name='contestant_list'),
    path('contestants/add/', views.add_contestant, name='add_contestant'),
    path('contestants/<int:contestant_id>/rate/', views.rate_contestant, name='rate_contestant'),
    path('assign/', views.assign_contestants_to_user, name='assign_contestants'),

]