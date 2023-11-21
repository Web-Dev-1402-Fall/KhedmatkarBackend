from django.urls import path, include
from .views import *

urlpatterns = [
    path('spec/add/', NewSpecialityView.as_view()),
]
