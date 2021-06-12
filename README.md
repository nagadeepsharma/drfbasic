# Django Rest FrameWork
# Topics [Custom User Model,Custom User Forms,TokenAuthentication]

# Custom User Model
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("email or username must be provided")
        email=self.normalize_email(email)
        user=self.model(email=email,++extra_fields)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email,password, **extra_fields)
        
class CustomUser(AbstractUser):

    username=None
    email=models.EmailField(verbose_name="email",unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()
    
    def __str__(self):
        return self.email

        
# settings.py

AUTH_USER_MODEL='accounts.CustomUser'

# admin.py

from django.contrib.auth import get_user_model
User=get_user_model()
admin.site.register(User)

# Custom User Form
# forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

# TokenAuthentication
# serializers.py

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import exceptions
from django.utils import timezone
User=get_user_model()

class Registerserializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self,data):
        username=data.get('username','')
        password=data.get('password','')
        if not User.objects.filter(email=username):
            if username and password:
                user=User.objects.create(email=username)
                user.set_password(password)
                user.save()
                data['message']='successfully registered'
                return data
            else:
                msg="Username and Password must provide"
                raise exceptions.ValidationError(msg)
        else:
            msg="User already Exists!"
            raise exceptions.ValidationError(msg)
            
class Loginserializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self,data):
        username=data.get('username','')
        password=data.get('password','')
        if username and password:
            user=authenticate(email=username,password=password)
            if user:
                data['user']=user
                user.last_login=timezone.now()
                user.save()
                return data
            else:
                msg="Username and Password Invalid"
                raise exceptions.ValidationError(msg)
        else:
            msg="Username and Password must provide"
            raise exceptions.ValidationError(msg)

# settings.py

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# views.py

from drfbasic.serializers import Registerserializer
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .serializers import Registerserializer,Loginserializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status,exceptions


class Index(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        return Response({'message':'Welcome to Django rest Framework'})
        
    def post(self,request):
        contact=request.data.get('contact')
        return Response({'Contact':contact})

    

@api_view(['POST'])

def register(request):
    regs=Registerserializer(data=request.data)
    regs.is_valid(raise_exception=True)
    message=regs.validated_data['message']
    return Response({'message':message})

@api_view(['POST'])

def login(request):
    regs=Loginserializer(data=request.data)
    regs.is_valid(raise_exception=True)
    user=regs.validated_data['user']
    token, created=Token.objects.get_or_create(user=user)
    return Response({'token':token.key})


@permission_classes(['isAuthenticated'])
@authentication_classes(['TokenAuthentication'])
@api_view(['GET'])

def logout(request):
    print(request.user)
    if(str(request.user)!='AnonymousUser'):
        request.user.auth_token.delete()
        return Response({'status':'logout sucessfull'})
    else:
        raise exceptions.ValidationError("invalid user")
