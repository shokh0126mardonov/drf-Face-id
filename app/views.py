from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .permissons import IsAdmin,IsSuperAdmin
from .serializers import LoginSerializer

class LoginViewSets(APIView):
    def post(self,request:Request)->Response:
        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            user = authenticate(username = data['username'],password = data['password'])

            if user is not None:
                token,created = Token.objects.get_or_create(user = user)
                return Response({'token':token.key},status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_404_NOT_FOUND)