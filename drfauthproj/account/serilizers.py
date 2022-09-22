from rest_framework import serializers

from account.utils import Util
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# While User Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    # This field is for confirmation of password
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc'] # all these fields should be in 'def create_user' in models.py
        extra_kwargs = {'password': {'write_only':True}}

    # Validating password and password2 while registrating the user
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        return attrs

    # Since we are using custom create user
    # We have to create user here too
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

# User Login
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

# Just to see User Profile (GET)   
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

# To Change/Rest user password
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_style': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'inpyt_style': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user') # user from context from views.py
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        user.set_password(password)
        user.save()
        return attrs

# To send reset password link to email
class SendPasswordRestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id)) # uid will be in bytecode
            print("Encoded UID: ", uid)
            print("Encoded UID: ", type(uid))
            token = PasswordResetTokenGenerator().make_token(user)
            print("Token: ", token)
            print("Token: ", type(token))
            link = "http://localhost:3000/api/user/reset/"+uid+"/"+token+"/"
            print("Password reset link:", link)

            # Send Email (created in utils.py file)
            body = "Click on following link to Reset Your Password " + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_mail(data) # in utils.py
            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')

# To change/reset the password by clicking on rest-password-link from email
class UserPasswordResetSerializer(serializers.Serializer):
    try:          
        password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
        password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
        class Meta:
            model = User
            fields = ['password', 'password2']

        def validate(self, attrs):
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid') # this 'uid' is in bytecode. It's Encoded. we have to decode it
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password don't match. Please check again")

            id = smart_str(urlsafe_base64_decode(uid)) # Decoding the uid
            user = User.objects.get(id=id)
            # We used make_token() to create token
            # Using check_token() to check token
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not Valid or Expired")
            user.set_password(password)
            user.save()
            return attrs
    except DjangoUnicodeDecodeError as idetifier:
        # This try and except are Extra layer of security
        PasswordResetTokenGenerator().check_token()
        raise serializers.ValidationError("Token is not Valid or Expired")

