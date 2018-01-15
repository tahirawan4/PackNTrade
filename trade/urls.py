from django.contrib import admin
from django.urls import path

from trade.views import home

urlpatterns = [
    path('home/', home, name='index'),
]
