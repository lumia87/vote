# vote_app/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vote_app',  # Ứng dụng của bạn
]

AUTH_USER_MODEL = 'vote_app.CustomUser'  # CustomUser là mô hình người dùng trong vote_app
