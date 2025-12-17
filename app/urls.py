from django.urls import path
from .views import LoginViewSets,AdminCreate,LogoutViewSets,ProfileViewSets,PasswordChangeViewSets
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/',LoginViewSets.as_view()),
    path('create/',AdminCreate.as_view()),
    path('logout/',LogoutViewSets.as_view()),
    path('profile/',ProfileViewSets.as_view()),
    path('password-change/',PasswordChangeViewSets.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)