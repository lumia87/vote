from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, OTPVerificationForm, LoginForm, ScoreForm
from .forms import AssignContestantsForm
from vote_app2.backends import ContestantBackend, CustomUserBackend  # Import your backends

from django.contrib.admin.views.decorators import staff_member_required

from vote_app2.models import Contestant, Score
from django.contrib.auth import get_user_model
from .models import Contestant, Assignment

from django.urls import reverse

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

            # Attempt login with ContestantBackend
            contestant_user = ContestantBackend.authenticate(request, email=email, password=password)
            if contestant_user is not None:
                login(request, contestant_user, backend='vote_app2.backends.ContestantBackend')
                return redirect('vote_app2:contestant_home')

            # Attempt login with CustomUserBackend
            custom_user = CustomUserBackend.authenticate(request, email=email, password=password)

            if custom_user is not None:
                login(request, custom_user, backend='vote_app2.backends.CustomUserBackend')
                if custom_user.is_staff:
                    return redirect('vote_app2:view_all_scores')
                else:
                    return redirect('vote_app2:user_home')
        else:
            form.add_error(None, 'Không đúng email/password')
    else:
        form = LoginForm()
    
    return render(request, 'vote_app2/login.html', {'form': form})

@login_required
def view_all_scores(request):
    if not request.user.is_staff:
        return redirect('vote_app2:user_home')  # Non-staff users should not access this page
    scores = Score.objects.all().select_related('contestant', 'user')
    return render(request, 'vote_app2/view_all_scores.html', {'scores': scores})


@login_required
def contestant_home(request):
    contestant = request.user
    if not isinstance(contestant, Contestant):
        return redirect('vote_app2:login')

    scores = Score.objects.filter(contestant=contestant)
    return render(request, 'vote_app2/contestant_home.html', {'scores': scores})

@login_required
def home_view(request):
    user = request.user
    assignments = Assignment.objects.filter(user=user)
    assigned_contestants = [assignment.contestant for assignment in assignments]
    print(assigned_contestants)
    if request.method == 'POST':
        
        form = ScoreForm(request.POST, user=request.user)
        if form.is_valid():
            print('form valid')
            form.save(commit=True)  # Save the form data to the database

            score = form.cleaned_data['score']
            contestant = form.cleaned_data['contestant']

            # Fetch all scores for the user and contestant
            scores = Score.objects.filter(user=user, contestant=contestant)

            if scores.exists():
                # Update the first found score object
                score_obj = scores.first()
                score_obj.score = score
                score_obj.save()
            else:
                # Create a new score object if none exists
                Score.objects.create(user=user, contestant=contestant, score=score)

            # Refresh assigned contestants after saving the form
            # assignments = Assignment.objects.filter(user=user)
            # assigned_contestants = [assignment.contestant for assignment in assignments]
        else:
            print('scoreform not valid')
    else:
        # Fetch assigned contestants again in case of redirect
        form = ScoreForm(initial={'user': request.user.pk}, assigned_contestants=assigned_contestants)  # Initialize form with user pk
    
    # Retrieve all scores for the logged-in user's contestants
    user_scores = {}
    for contestant in assigned_contestants:
        scores = Score.objects.filter(user=user, contestant=contestant)
        user_scores[contestant.id] = scores.last() if scores.exists() else None

    return render(request, 'vote_app2/user_home.html', {'form': form, 'contestants': assigned_contestants, 'user_scores': user_scores, 'user': user})


def logout(request):
    return redirect(reverse('vote_app2:login'))


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

@staff_member_required
def assign_contestants_to_user(request):
    if request.method == 'POST':
        form = AssignContestantsForm(request.POST)
        if form.is_valid():
            contestants = form.cleaned_data['contestants']
            judge = form.cleaned_data['judge']
            for contestant in contestants:
                # Check if an assignment already exists
                if not Assignment.objects.filter(user=judge, contestant=contestant).exists():
                    Assignment.objects.create(user=judge, contestant=contestant)
            # return redirect('vote_app2:user_home')  # Replace 'success_url' with the URL to redirect to after successful submission
    else:
        form = AssignContestantsForm()

   # Lấy danh sách các thí sinh đã được phân công và chưa được phân công
    all_contestants = Contestant.objects.all()
    assigned_contestants = Assignment.objects.values_list('contestant', flat=True)
    unassigned_contestants = all_contestants.exclude(id__in=assigned_contestants)

    assignments = Assignment.objects.select_related('user', 'contestant')

    context = {
        'form': form,
        'assignments': assignments,
        'unassigned_contestants': unassigned_contestants,
    }

    return render(request, 'vote_app2/assign_contestants.html', context)