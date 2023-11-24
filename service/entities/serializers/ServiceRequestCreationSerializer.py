from rest_framework import serializers


class ServiceRequestCreationSerializer(serializers.Serializer):
    specialty_id = serializers.IntegerField(required=True)
    description = serializers.CharField(required=False)
    address = serializers.CharField(required=True)
    reception_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=True)
    specialist_id = serializers.IntegerField(required=False)
