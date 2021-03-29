from django.contrib import admin
from django.urls import path, include
from django.views.generic import base
import hello.views as hello


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include('hello.urls')),
    path('', hello.index),
    path('accounts/login/', base.RedirectView.as_view(pattern_name="hello:login")),
    path('accounts/profile/', base.RedirectView.as_view(pattern_name="hello:index")),    
]
