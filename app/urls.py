from django.urls import path
from .views import LoginViewSets,AdminCreate,LogoutViewSets,ProfileViewSets,PasswordChangeViewSets

urlpatterns = [
    path('login/',LoginViewSets.as_view()),
    path('create/',AdminCreate.as_view()),
    path('logout/',LogoutViewSets.as_view()),
    path('profile/',ProfileViewSets.as_view()),
    path('password-change/',PasswordChangeViewSets.as_view()),
]