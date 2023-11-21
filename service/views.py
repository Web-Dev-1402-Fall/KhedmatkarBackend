from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from service.entities.serializers.SpecialtySerializer import SpecialtySerializer
from user.decorators import admin_required


# Create your views here.
class NewSpecialityView(APIView):
    permission_classes = [IsAuthenticated,]

    @admin_required
    def post(self, request):
        specialty = SpecialtySerializer(data=request.data)
        specialty.is_valid()
        return Response(status.HTTP_200_OK)
