from django.contrib import admin
from django.urls import path

from main.views import View

urlpatterns = [
    path('', View.dashboard),
    path('dashboard', View.dashboard),
    path('about us', View.about_us)
]