from rest_framework import serializers
from .models import Person

(serializers.ModelSerializer
class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()
    address = serializers.CharField(max_length=200)
    subject = serializers.ChoiceField(choices=Person.subject_choices)

    # TODO: remove these overrides
    # These are only called from .save() function
    def create(self, validated_data):
        # mosty called while creation of new entities (POST)
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # update is called during PATCH, PUT
        # instance is the existing info from DB
        # validated_data is the data from the request
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.address = validated_data.get('address', instance.address)
        instance.subject = validated_data.get('subject', instance.subject)

        instance.save()
        return instance
