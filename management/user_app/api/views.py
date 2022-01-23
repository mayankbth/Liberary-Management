from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from user_app.api.serializers import RegistrationSerializer
# from django.contrib.auth
# from user_app import models

@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):
    print(request.user.pk)
    if request.user.pk == None:
        print(request.user)
        if request.method == 'POST':
            serializer = RegistrationSerializer(data=request.data)
            # here I am accessing the token from the models.py
            data = {}
            if serializer.is_valid():
                account = serializer.save()
                data['response'] = 'Registration Successful!'
                data['username'] = account.username
                data['email'] = account.email
                refresh = RefreshToken.for_user(account)
                data['token'] = {
                                    'refresh': str(refresh),
                                    'access': str(refresh.access_token),
                                }
            else:
                data = serializer.errors
            return Response(data)
    else:
        print(request.user)
        return Response("You can not create a new user while logged in.")

