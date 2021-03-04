from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
