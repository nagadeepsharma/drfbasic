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
