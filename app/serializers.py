from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Student, Rules, Payment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "groups",
            "user_permissions",
            "is_staff",
            "is_superuser",
            "last_login",
            "password",
            "role",
            "date_joined",
            "is_active",
        ]


class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password",
            "role",
            "groups",
            "user_permissions",
            "is_staff",
            "is_superuser",
        ]
        extra_kwargs = {"username": {"required": False}}


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    confirm = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm"]:
            raise serializers.ValidationError("Password va confirm teng emas!")
        return super().validate(attrs)


class StudentSerializers(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)

    class Meta:
        model = Student
        exclude = ["created_at", "updated_at"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None


class RulesSerializers(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)

    class Meta:
        model = Rules
        fields = ["id", "gender", "login_time", "exit_time", "admin"]


class PaymentSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)  # POST uchun
    student = StudentSerializers(read_only=True)  # GET uchun

    class Meta:
        model = Payment
        fields = [
            "id",
            "admin",
            "student",
            "student_id",
            "amount",
            "month",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        student_id = validated_data.pop("student_id")
        student = Student.objects.get(id=student_id)
        return Payment.objects.create(student=student, **validated_data)


class TrackingSerializers(serializers.Serializer):
    token = serializers.CharField()
    status = serializers.CharField()
