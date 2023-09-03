from .models import *
from rest_framework import serializers


class fuzzyModelSerializer(serializers.Serializer):
    experience = serializers.IntegerField()
    numberОfСlients = serializers.IntegerField()
    border1 = serializers.IntegerField()
    border2 = serializers.IntegerField()
    border3 = serializers.IntegerField()
    norma = serializers.IntegerField()
    hours = serializers.IntegerField()