from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'vote_app2'  # Đặt tên namespace cho ứng dụng

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('otp_verification/<int:user_id>/', views.otp_verification, name='otp_verification'),
    path('assign/', views.assign_contestants_to_user, name='assign_contestants'),
    path('view_all_scores/', views.view_all_scores, name='view_all_scores'), #trang của admin
    path('user_home/', views.home_view, name='user_home'), #trang của giám khảo
    path('contestant_home/', views.contestant_home, name='contestant_home'), #trang của thí sinh

]