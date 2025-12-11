from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .permissons import IsAdmin,IsSuperAdmin
from .serializers import LoginSerializer,RegisterSerializers,UserSerializer,ProfileSerializer,PasswordChangeSerializer


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
    

class AdminCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = [IsSuperAdmin]

    def post(self,request:Request)->Response:
        serializer = RegisterSerializers(data = request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_data = UserSerializer(user).data

            return Response(data=user_data,status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class LogoutViewSets(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def post(self,request:Request)->Response:
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProfileViewSets(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self,request:Request)->Response:
        serializer = ProfileSerializer(request.user).data
        return Response(data=serializer)

    def put(self,request:Request)->Response:
        user = request.user
        serializer = ProfileSerializer(data = request.data,partial=True)

        if serializer.is_valid(raise_exception=True):
            update_user = serializer.update(user,serializer.validated_data)

        serializer = UserSerializer(update_user).data
        return Response(serializer,status=status.HTTP_204_NO_CONTENT)
    
class PasswordChangeViewSets(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request:Request)->Response:
        serilizers = PasswordChangeSerializer(data = request.data)

        if serilizers.is_valid(raise_exception=True):
            data = serilizers.validated_data

            user = request.user
            user.set_password(data['password'])     
            user.save()   
            serilizer = UserSerializer(user)
            return Response(serilizer.data, status=status.HTTP_204_NO_CONTENT)
