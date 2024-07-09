
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('app1/', include('vote_app.urls')),
    path('', include('vote_app2.urls')), #ưu tiên 2


]
