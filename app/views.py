from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response


class InitViewsets(ViewSet):
    def post(self,request:Request)->Response:
        return Response({})