from .models import Calendar2019
from rest_framework import serializers, viewsets

class Calendar2019Serializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar2019
        fields = '__all__'

class Calendar2019ViewSet(viewsets.ModelViewSet):
    queryset = Calendar2019.objects.all()
    serializer_class = Calendar2019Serializer

