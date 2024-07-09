from django import forms
from .models import CustomUser
from .models import Contestant
from .models import Score, Assignment

from django.utils import timezone

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose a different one.")
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='OTP', required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if not self.user.verify_otp(otp):
            raise ValidationError("Invalid OTP")
        return otp

class ContestantLoginForm(AuthenticationForm):
    class Meta:
        model = Contestant
        fields = ['username', 'password']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = None

        # Try to get the user from CustomUser model
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            pass

        # If not found in CustomUser, try to get from Contestant model
        if user is None:
            try:
                user = Contestant.objects.get(email=email)
            except Contestant.DoesNotExist:
                raise ValidationError("Invalid email or password")

        # Check password
        if not check_password(password, user.password):
            raise ValidationError("Invalid email or password")

        # Check if the user is verified
        if not user.is_verified:
            raise ValidationError("Account not verified. Please verify your account.")

        # Set the user in the cleaned_data for use in the view
        self.cleaned_data['user'] = user
        return self.cleaned_data


class ContestantLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        print('pw theo form contest',password)
        try:
            contestant = Contestant.objects.get(email=email)
            print(contestant.password)
        except Contestant.DoesNotExist:
            raise ValidationError("Invalid email")
        if not check_password(password, contestant.password):
            raise ValidationError("Invalid password")
        if not contestant.is_verified:
            raise ValidationError("Account not verified. Please verify your account.")
        print(self.cleaned_data)
        return self.cleaned_data


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score', 'user', 'contestant']
        widgets = {
            'user': forms.HiddenInput(),  # Hide the user field in the form
        }

    def __init__(self, *args, user=None, assigned_contestants=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = user.pk if user else None
        if user:
            # Get assigned contestants for the current user
            assigned_contestants = Assignment.objects.filter(user=user).values_list('contestant', flat=True) #tra ve list IDs of the contestants gan voi user cu the. 
            print(assigned_contestants)
            # Filter contestants by assigned ids
            self.fields['contestant'].queryset = Contestant.objects.filter(id__in=assigned_contestants) #loc cac id trong contestant cho scoreform
        elif (assigned_contestants is not None):
            self.fields['contestant'].queryset = Contestant.objects.filter(email__in=assigned_contestants)    

    def save(self, commit=True):

        instance = super().save(commit=False)
        instance.timestamp = timezone.now()  # Update the timestamp to current time

        if commit:
            instance.save()

        return instance
    

class AssignContestantsForm(forms.Form):
    contestants = forms.ModelMultipleChoiceField(queryset=Contestant.objects.all(), widget=forms.CheckboxSelectMultiple, label="Thí sinh")
    #staff để quản trị, khởi tạo ds giám khảo, các user thường mới chấm
    judge = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_staff=False), label="Người đánh giá")