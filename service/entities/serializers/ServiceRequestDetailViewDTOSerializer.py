from rest_framework import serializers
from service.entities import ServiceRequest, Specialty  # Corrected import path


class ServiceRequestDetailViewDTOSerializer(serializers.ModelSerializer):
    specialty_brief = serializers.CharField(source='specialty.name')  # Directly get the name if you need only that

    class Meta:
        model = ServiceRequest
        fields = ['id', 'specialty_brief', 'description', 'address']
