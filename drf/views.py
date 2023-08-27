from rest_framework.response import Response
from rest_framework.request import Request
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Person
from .serializers import PersonSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.versioning import NamespaceVersioning
from rest_framework.exceptions import PermissionDenied
from .exceptions import InvalidPersonDetailsException
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .permissions import HasUpdatedOrNoOwner
from .pagination import CustomPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from time import sleep
from .tasks import drf_sleeping_task

User = get_user_model()


class CustomVersioning(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']

########### Views sets #################


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # TODO: only allow superusers to do any operation here
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'users'


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        # permissions.IsAuthenticatedOrReadOnly, 
        HasUpdatedOrNoOwner
    ]
    # versioning_class = CustomVersioning
    # lookup_url_kwarg = 'pk'
    pagination_class = CustomPagination
    throttle_scope = 'person'

    @method_decorator(cache_page(5))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        print(f"X For {request.META.get('HTTP_X_FORWARDED_FOR')}")
        print(f"Remote addr {request.META.get('REMOTE_ADDR')}")
        # sleep(20) # long running thing that can be processed in background
        drf_sleeping_task.delay() # hand over to celery
        return super().retrieve(request, *args, **kwargs)

    # This was to showcase throwing exceptions
    # def retrieve(self, request, *args, **kwargs):
    #     if request.version:
    #         if request.version == 'v1':
    #             print(f"This version is the old implementation")
    #         if request.version == 'v2':
    #             print(f"This version is the new implementation")
    #     # return super().retrieve(request, *args, **kwargs)
    #     # return Response(status=status.HTTP_400_BAD_REQUEST)
    #     # raise PermissionDenied(detail="Overriding retreive for testing")
    #     raise InvalidPersonDetailsException(detail="Custom invalid request")


########### Class based Views with Generic Views #################


class PeopleDetailsUsingGenerics(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetailsUsingGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_url_kwarg = 'person'


########### Class based Views with Mixins #################


class PeopleDetailsUsingMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # fetch DB objects (bulk/single)
    # using serialiser
    # sending response
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get(self, request: Request, format=None, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonDetailsUsingMixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_url_kwarg = 'person'

    def get(self, request: Request, format=None, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


########### Class based Views #################


class PeopleDetails(APIView):
    def get(self, request: Request, format=None):
        people = Person.objects.all()
        # deserialisation (DB -> JSON Response)
        ser_response = PersonSerializer(people, many=True)
        return Response(ser_response.data)

    def post(self, request: Request, format=None):
        # ser [data format (JSON/FORM) request -> DB]
        ser_request = PersonSerializer(data=request.data)
        if not ser_request.is_valid():
            return Response(ser_request.errors, status=status.HTTP_400_BAD_REQUEST)

        # this is serilializer save
        ser_request.save()
        return Response(ser_request.data, status=status.HTTP_201_CREATED)


class PersonDetails(APIView):
    def get_object(self, person_id: int):
        try:
            person = Person.objects.get(pk=person_id)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return person

    def get(self, request: Request, person_id: int, format=None):
        person = self.get_object(person_id)
        ser_response = PersonSerializer(person)
        return Response(ser_response.data)

    def put(self, request: Request, person_id: int, format=None):
        person = self.get_object(person_id)
        ser_response = PersonSerializer(person, data=request.data)
        if not ser_response.is_valid():
            return Response(ser_response.errors, status=status.HTTP_400_BAD_REQUEST)

        ser_response.save()
        return Response(ser_response.data, status=status.HTTP_201_CREATED)

    def delete(self, request: Request, person_id: int, format=None):
        person = self.get_object(person_id)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

########### Function based Views #################


@api_view(['GET', 'POST'])
@csrf_exempt
def people_details(request: Request, format=None):
    if request.method == 'GET':
        people = Person.objects.all()
        # deserialisation (DB -> JSON Response)
        ser_response = PersonSerializer(people, many=True)
        return Response(ser_response.data)

    elif request.method == 'POST':
        # ser [data format (JSON/FORM) request -> DB]
        ser_request = PersonSerializer(data=request.data)
        if not ser_request.is_valid():
            return Response(ser_request.errors, status=status.HTTP_400_BAD_REQUEST)

        # this is serilializer save
        ser_request.save()
        return Response(ser_request.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def person_details(request: Request, person_id: int, format=None):
    try:
        person = Person.objects.get(pk=person_id)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ser_response = PersonSerializer(person)
        return Response(ser_response.data)

    if request.method in ['PUT', 'PATCH']:
        partial = False
        if request.method == 'PATCH':
            partial = True
        ser_response = PersonSerializer(
            person, data=request.data, partial=partial)
        if not ser_response.is_valid():
            return Response(ser_response.errors, status=status.HTTP_400_BAD_REQUEST)

        ser_response.save()
        return Response(ser_response.data, status=status.HTTP_201_CREATED)

    if request.method == "DELETE":
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
