from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import permissions, status
from .serializers import  UserSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CreateUserAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    POST auth/signup/
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):

        try:
            username = request.data['username']
            password = request.data['password']
            print(username)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    user_details = {'token': token}
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and a password'}
            return Response(res)


class SignUpView(APIView):
    """
    POST auth/signup/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)