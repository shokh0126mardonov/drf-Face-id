from django.urls import path
from .views import (
    LoginViewSets,
    AdminCreate,
    LogoutViewSets,
    ProfileViewSets,
    PasswordChangeViewSets,
    StudentViewSets,
    RulesviewSets,
    PaymentsViewSets,
    TruckingViewSets
    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Adminka
    path('login/',LoginViewSets.as_view()),
    path('create/',AdminCreate.as_view()),
    path('logout/',LogoutViewSets.as_view()),
    path('profile/',ProfileViewSets.as_view()),
    path('password-change/',PasswordChangeViewSets.as_view()),

    #Rules Crud
    path('rules/',RulesviewSets.as_view({'get': 'list', 'post': 'create'})),
    path('rules/<int:pk>/',RulesviewSets.as_view({'get': 'retrieve', 'put': 'update','delete':'destroy'})),

    # User Crud
    path('students/',StudentViewSets.as_view({'get': 'list', 'post': 'create'})),
    path('students/<int:pk>/',StudentViewSets.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    #Payments
    path('payment/',PaymentsViewSets.as_view({'get': 'list', 'post': 'create'})),
    path('payment/<int:pk>/',PaymentsViewSets.as_view({'get': 'retrieve', 'put': 'update'})),

    #Truckings
    path('trucking/',TruckingViewSets.as_view())
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)