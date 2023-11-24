from rest_framework import serializers

from service.entities.Specialty import Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'

    def create(self, validated_data):
        return Specialty.objects.create(**validated_data)