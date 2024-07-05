# from django.contrib.auth import login
from django.shortcuts import render, redirect
# from django.urls import reverse
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
import urllib.parse
# Đảm bảo import từ django.utils.encoding

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ScoreForm
from .models import Score
import random
from datetime import datetime  # Import module datetime
from pymongo import MongoClient

from django.core.mail import send_mail
from .forms import CustomUserCreationForm, OTPForm
from .models import CustomUser

def generate_otp():
    return str(random.randint(100000, 999999))

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.otp = generate_otp()
            user.save()
            send_otp_email(user, request)
            return redirect('enter_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'vote_app/register.html', {'form': form})

def send_otp_email(user, request):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {user.otp}'
    send_mail(subject, message, 'webmaster@localhost', [user.email])


def enter_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            user = CustomUser.objects.filter(otp=otp).first()
            if user:
                user.is_active = True
                user.otp = None
                user.save()
                login(request, user)
                return redirect('home')
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'vote_app/enter_otp.html', {'form': form})

@login_required
def user_list(request):
    users = CustomUser.objects.all()  # Lấy tất cả người dùng từ cơ sở dữ liệu
    return render(request, 'vote_app/user_list.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('user_list')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Chuyển hướng đến trang chủ sau khi đăng nhập thành công
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'vote_app/login.html', {'form': form})


@login_required
def home(request):
    success_message = ""
    error_message = ""
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score_value = form.cleaned_data['score']
            timestamp=datetime.now()

            # Thay thế các giá trị thực tế của username, password, cluster_name
            username = "lumia"
            password = "Linhchi87"
            cluster_name = "cluster1"

            # Mã hóa username và password
            quoted_username = urllib.parse.quote_plus(username)
            quoted_password = urllib.parse.quote_plus(password)

            # Tạo MongoDB URI
            mongo_uri = f"mongodb+srv://{quoted_username}:{quoted_password}@{cluster_name}.vidjqep.mongodb.net/?retryWrites=true&w=majority"

            try:
                # Kết nối đến MongoDB
                client = MongoClient(mongo_uri)
                mongo_db = client.get_database('vote')
                mongo_collection = mongo_db['scores']

                # Lưu điểm vào MongoDB
                result = mongo_collection.insert_one({
                    'user_id': request.user.id,
                    'email': request.user.email,
                    'score': score_value,
                    'timestamp': timestamp # Thêm timestamp
                })

                if result.acknowledged:
                    success_message = "Lưu điểm vào MongoDB thành công."
                else:
                    error_message = "Lưu điểm vào MongoDB thất bại."

                # Lưu điểm vào Django model
                score = form.save(commit=False)
                score.user = request.user
                score.timestamp = timestamp  # Add timestamp to Django model
                score.save()

                return redirect('home')  # Chuyển hướng lại đến trang home sau khi lưu điểm thành công.
            
            except Exception as e:
                error_message = f"Đã xảy ra lỗi khi lưu điểm vào MongoDB: {str(e)}"
    else:
        form = ScoreForm()
    # Get user's scores
    user_scores = Score.objects.filter(user=request.user)
    context = {
        'form': form,
        'user_scores': user_scores,
        'username':request.user.email,
        'success_message': success_message,
        'error_message': error_message,
    }
    return render(request, 'vote_app/home.html', context)