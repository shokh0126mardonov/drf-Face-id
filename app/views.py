from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


class InitViewsets(APIView):
    
    def post(self,request:Request)->Response:
        return Response(request.data)
    
    def get(self,request:Request)->Response:
        return Response('Salom')