from django.shortcuts import render, redirect

from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, OTPVerificationForm, LoginForm, ScoreForm
from .forms import ContestantForm

from vote_app2.models import Contestant, Score, CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

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
    if request.method == 'POST':
        
        form = ScoreForm(request.POST, user=request.user)
        if form.is_valid():
            score = form.cleaned_data['score']
            contestant = form.cleaned_data['contestant']
            # user = request.user  # Assume the logged-in user

            # Save the score for the contestant
            score_obj, created = Score.objects.get_or_create(user=request.user, contestant=contestant, defaults={'score': score})
            if not created:
                score_obj.score = score
                score_obj.save()

            # Refresh contestant list
            contestants = Contestant.objects.all()

            # Return updated data to the template
            return render(request, 'vote_app2/home.html', {'form': form, 'contestants': contestants})
    else:
        # form = ScoreForm()
        form = ScoreForm(initial={'user': request.user.pk})  # Initialize form with user pk
        contestants = Contestant.objects.all()

    return render(request, 'vote_app2/home.html', {'form': form, 'contestants': contestants})

def contestant_list(request):
    contestants = Contestant.objects.all()
    return render(request, 'vote_app2/home.html', {'contestants': contestants})

def add_contestant(request):
    if request.method == 'POST':
        form = ContestantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vote_app2:contestant_list')
    else:
        form = ContestantForm()
    return render(request, 'vote_app2/add_contestant.html', {'form': form})

@login_required
def rate_contestant(request, contestant_id):
    contestant = get_object_or_404(Contestant, id=contestant_id)
    user = request.user  # Giả sử người dùng đã đăng nhập
    if request.method == 'POST':
        print(contestant, user)
        if isinstance(user, User):  # Kiểm tra nếu user là instance của model User
            score_value = int(request.POST.get('score'))
            score, created = Score.objects.get_or_create(user=user, contestant=contestant, defaults={'score': score_value})
            if not created:
                score.score = score_value
                score.save()
            return redirect('vote_app2:contestant_list')
        else:
            raise ValueError("The user is not an instance of the User model")
    return render(request, 'vote_app2/rate_contestant.html', {'contestant': contestant})