from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Username
from .serializer import UsernameSerializer

@api_view(['GET'])
def get_usernames(request):
    usernames = Username.objects.all()
    serializedData = UsernameSerializer(usernames, many=True).data
    return Response(serializedData)