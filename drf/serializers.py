from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()
    address = serializers.CharField(max_length=200)
    subject = serializers.ChoiceField(choices=Person.subject_choices)

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
