from django.urls import path
from .views import LoginViewSets

urlpatterns = [
    path('login/',LoginViewSets.as_view())
]