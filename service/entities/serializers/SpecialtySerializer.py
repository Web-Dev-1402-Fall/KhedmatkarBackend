from rest_framework import serializers


class SpecialtySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=True)
    parent_id = serializers.IntegerField(required=False)
