from django.shortcuts import render, redirect
from .forms import RegistrationForm, OTPVerificationForm, LoginForm
from .models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.generate_otp()
            send_otp(user)
            return redirect('vote_app2:otp_verification', user_id=user.id)
    else:
        form = RegistrationForm()
    return render(request, 'vote_app2/register.html', {'form': form})

def otp_verification(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST, user=user)
        if form.is_valid():
            return redirect('vote_app2:login')
    else:
        form = OTPVerificationForm(user=user)
    return render(request, 'vote_app2/otp_verification.html', {'form': form})

def send_otp(user):
    otp = user.otp
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('vote_app2:home')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'vote_app2/login.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'vote_app2/home.html')