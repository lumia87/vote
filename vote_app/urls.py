from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'vote_app'  # Đặt tên namespace cho ứng dụng

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('enter_otp/', views.enter_otp, name='enter_otp'),
    path('user_list/', views.user_list, name='user_list'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('home/', views.home, name='home'),  # Ensure you have a 'home' view defined
]