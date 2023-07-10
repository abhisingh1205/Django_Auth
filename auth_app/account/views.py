from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerialzer, SendPasswordResetSerializer, UserPasswordResetSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#get token SImple JWT manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg': 'Registration Success', 'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            
            user = authenticate(email=email, password=password)
            
            token = get_tokens_for_user(user)
            

            if user is not None:
                return Response({'msg': 'Login Successfull', 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)



class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerialzer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
        

class SentPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            return Response({'msg': 'Password Reset email link sent. Plese check email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(get, request, uid, token, format= None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token': token})
        
        if serializer.is_valid():
            return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)