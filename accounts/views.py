from rest_framework.views import APIView
from accounts.models import Works
from accounts.serializers import  Workserializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class index(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data=Works.objects.filter(user=self.request.user)
        ws=Workserializer(data,many=True)
        return Response(ws.data)
    def post(self,request):
        if not request.data.get('designation'):
            raise ValidationError("Invalid Designation")
        data=Works.objects.create(designation=request.data.get('designation'),user=request.user)
        wps=Workserializer(data)
        return Response(wps.data)


