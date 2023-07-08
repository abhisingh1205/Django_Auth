from rest_framework import serializers
from .models import User
from .utils import Util
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ["email", "name", "password", "password2", "tc"]

        extra_kwargs = {
            'password': {'write_only':True}
        }
    
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError('Password and confirm password does not match')
        
        return data
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name"]


class UserChangePasswordSerialzer(serializers.Serializer):
    password = serializers.CharField(max_length=250, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=250, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password  and Confirm Password does not match')
        
        user.set_password(password)
        user.save()

        return attrs 
    
class SendPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://localhost:3000/api/user/reset/" + uid + "/" + token
            print("Password Link = ", link)

            body = 'Click following link to reset your password ' + link
            data = {
                'subject' : 'Reset your password',
                'body': body,
                'to_email': user.email
            }

            #Send Email Code
            Util.send_email(data)
            return (attrs)             

        else:
            raise serializers.ValidationError('You are not a Registered User')
        


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=250, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=250, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError('Password  and Confirm Password does not match')
            uid = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=uid)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not valid or expired')
            
            user.set_password(password)
            user.save()

            return attrs
        
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')


        