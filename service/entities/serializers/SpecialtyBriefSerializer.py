from rest_framework import serializers


class SpecialtyBriefSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
