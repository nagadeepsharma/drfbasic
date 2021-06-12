
from accounts.models import Works
from rest_framework import serializers

class Workserializer(serializers.ModelSerializer):
    class Meta:
        model=Works
        fields='__all__'

