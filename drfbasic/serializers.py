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