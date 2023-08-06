from rest_framework import serializers
from .models import Person
from .exceptions import InvalidPersonDetailsException
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Person
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    people = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'people']
        read_only_fields = []
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password', ''))
        return super().create(validated_data)


class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()
    address = serializers.CharField(max_length=200)
    subject = serializers.ChoiceField(choices=Person.subject_choices)
    updated_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())

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
        instance.updated_by = validated_data.get(
            'updated_by', instance.updated_by)

        instance.save()
        return instance

    def validate(self, attrs):
        # This function is only called during serilaizer .is_valid()
        # add business validation
        age = attrs.get('age')
        if age and age > 50:
            raise InvalidPersonDetailsException(
                detail="People above 50 aren't allowed.")
        return super().validate(attrs)
