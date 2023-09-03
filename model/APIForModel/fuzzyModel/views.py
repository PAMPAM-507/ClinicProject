from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import fuzzyModel
from .Serializers import fuzzyModelSerializer
from .fuzzyModel2 import *


class APIFuzzyModelMiddleMax(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        ser = fuzzyModelSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        A1, A2, A3, B1, B2, B3 = solveInputValue(
            ser.validated_data.get('experience'),
            ser.validated_data.get('numberОfСlients'),
            ser.validated_data.get('border1'),
            ser.validated_data.get('border2'),
            ser.validated_data.get('border3'),
            ser.validated_data.get('norma'),
            ser.validated_data.get('hours'))

        answer = out_class(middleMax(getDefuzzification(ruleBase(A1, A2, A3, B1, B2, B3))))

        return Response({"answer": answer})


class APIFuzzyModelHeight(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        ser = fuzzyModelSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        A1, A2, A3, B1, B2, B3 = solveInputValue(
            ser.validated_data.get('experience'),
            ser.validated_data.get('numberОfСlients'),
            ser.validated_data.get('border1'),
            ser.validated_data.get('border2'),
            ser.validated_data.get('border3'),
            ser.validated_data.get('norma'),
            ser.validated_data.get('hours'))

        answer = out_class(Height(ruleBase(A1, A2, A3, B1, B2, B3)))

        return Response({"answer": answer})
    
    
class APIFuzzyModel2(APIView):

    def get(self, request):
        ser = fuzzyModelSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        A1, A2, A3, B1, B2, B3 = fuzzyModel.solveInputValue(
            ser.validated_data.get('hours'),
            ser.validated_data.get('numberОfСlients'),
            ser.validated_data.get('border1'),
            ser.validated_data.get('border2'),
            ser.validated_data.get('border3'),
            ser.validated_data.get('norma'))

        answer = fuzzyModel.middleMax(fuzzyModel.getDefuzzification(fuzzyModel.ruleBase(A1, A2, A3, B1, B2, B3)))

        return Response({"answer": answer})

# {
#     "experience": 8,
#     "numberОfСlients": 35,
#     "border1": 0,
#     "border2": 5,
#     "border3": 10,
#     "norma": 5,
#     "hours": 5
# }
