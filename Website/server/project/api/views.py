from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Username
from .serializer import UsernameSerializer
from django.shortcuts import render

@api_view(['GET'])
def get_usernames(request):
    usernames = Username.objects.all()
    serializedData = UsernameSerializer(usernames, many=True).data
    return Response(serializedData)

@api_view(['POST'])
def create_usernames(request):
    data = request.data
    serializer = UsernameSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])

def usernames_detail(request, pk):
    try :
        usernames = Username.objects.get(pk=pk)
    except Username.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE' :
        usernames.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = UsernameSerializer(usernames, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
