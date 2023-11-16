from rest_framework import serializers
from service.entities import Specialty


class SpecialtyBriefDTOSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name']  # Include the fields you want in the brief DTO
