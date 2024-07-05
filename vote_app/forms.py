from django import forms
from .models import CustomUser
from .models import Score
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class OTPForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6)

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score']



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_active', 'is_staff', 'is_superuser', 'otp')
