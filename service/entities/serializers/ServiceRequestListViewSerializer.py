from rest_framework import serializers
from service.entities import ServiceRequestStatus
from service.entities.serializers.SpecialtySerializer import SpecialtySerializer
from user.serializers import UserSerializer


class ServiceRequestListViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=ServiceRequestStatus.choices)
    creation = serializers.DateTimeField()
    address = serializers.CharField()
    reception_date = serializers.DateField()
    specialty = SpecialtySerializer()
    accepted_specialist = UserSerializer()
    candidate_specialist = UserSerializer()
