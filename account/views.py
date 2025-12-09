from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TestApiView(APIView):

    @extend_schema(
        summary="Test API endpoint",
        description="Returns a simple hello message",
        responses={200: dict}
    )
    def get(self, request):
        return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)
