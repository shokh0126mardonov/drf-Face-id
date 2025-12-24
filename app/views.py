from django.utils import timezone
from datetime import datetime

from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404

from .permissons import IsAdmin, IsSuperAdmin, IsAdmin_or_SuperAdmin
from .serializers import (
    LoginSerializer,
    RegisterSerializers,
    UserSerializer,
    ProfileSerializer,
    PasswordChangeSerializer,
    StudentSerializers,
    RulesSerializers,
    PaymentSerializer,
    TrackingSerializers,
)
from .models import Student, Rules, Payment, Tracking
from .filters import StudentFilter


class LoginViewSets(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            user = authenticate(username=data["username"], password=data["password"])

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_404_NOT_FOUND)


class AdminCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_data = UserSerializer(user).data

            return Response(data=user_data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSets(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin, IsAuthenticated]

    def post(self, request: Request) -> Response:
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewSets(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin_or_SuperAdmin]

    def get(self, request: Request) -> Response:
        serializer = ProfileSerializer(request.user).data
        return Response(data=serializer)

    def put(self, request: Request) -> Response:
        user = request.user
        serializer = ProfileSerializer(data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            update_user = serializer.update(user, serializer.validated_data)

        serializer = UserSerializer(update_user).data
        return Response(serializer, status=status.HTTP_204_NO_CONTENT)


class PasswordChangeViewSets(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin_or_SuperAdmin]

    def post(self, request: Request) -> Response:
        serilizers = PasswordChangeSerializer(data=request.data)

        if serilizers.is_valid(raise_exception=True):
            data = serilizers.validated_data

            user = request.user
            user.set_password(data["password"])
            user.save()
            serilizer = UserSerializer(user)
            return Response(serilizer.data, status=status.HTTP_204_NO_CONTENT)


class RulesviewSets(ModelViewSet):
    queryset = Rules.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin_or_SuperAdmin]
    serializer_class = RulesSerializers

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)


class StudentViewSets(ModelViewSet):
    queryset = Student.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin_or_SuperAdmin]
    serializer_class = StudentSerializers
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = StudentFilter

    search_fields = ["room", "token"]
    ordering_fields = ["room", "created_at"]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)


class PaymentsViewSets(ModelViewSet):
    queryset = Payment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin_or_SuperAdmin]
    serializer_class = PaymentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    def perform_create(self, serializer):
        student = Student.objects.get(id=self.request.data.get("student_id"))
        serializer.save(admin=self.request.user)


class TruckingViewSets(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin_or_SuperAdmin]

    def post(self, request: Request) -> Response:
        serilizers = TrackingSerializers(data=request.data)

        if serilizers.is_valid(raise_exception=True):
            data = serilizers.validated_data

            token = data["token"]
            status_ = data["status"]

            student = Student.objects.filter(token=token).first()

            if student is None:
                return Response("Student not found", status=status.HTTP_403_FORBIDDEN)

            rules = Rules.objects.get(gender=student.gender)

            if rules.login_time > rules.exit_time:
                if (
                    rules.login_time <= datetime.now().time()
                    or datetime.now().time() <= rules.exit_time
                ):
                    tracking = Tracking.objects.create(
                        student=student, status=status_, time=datetime.now()
                    )
                    return Response(
                        data=tracking.student.name, status=status.HTTP_201_CREATED
                    )
            elif rules.login_time < rules.exit_time:
                if rules.login_time <= datetime.now().time() <= rules.exit_time:
                    tracking = Tracking.objects.create(
                        student=student, status=status_, time=datetime.now()
                    )
                    return Response(
                        data=tracking.student.name, status=status.HTTP_201_CREATED
                    )

            print(datetime.now())
            return Response("Kiraverishingiz mumkin")
