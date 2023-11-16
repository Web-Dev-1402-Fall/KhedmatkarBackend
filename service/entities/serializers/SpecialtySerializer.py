from rest_framework import serializers


class SpecialtySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent_id = serializers.IntegerField(required=False)
