from django.urls import path
from .views import InitViewsets

urlpatterns = [
    path('',InitViewsets.as_view())
]