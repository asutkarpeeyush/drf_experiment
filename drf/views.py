from django.http import HttpRequest, JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Person
from .serializers import PersonSerializer
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET', 'POST'])
@csrf_exempt
def person_details(request: HttpRequest):
    if request.method == 'GET':
        people = Person.objects.all()
        # deserialisation (DB -> JSON Response)
        ser_response = PersonSerializer(people, many=True)
        return Response(ser_response.data)

    elif request.method == 'POST':
        # ser [data format (JSON/FORM) request -> DB]
        ser_request = PersonSerializer(data=request.data)
        if not ser_request.is_valid():
            print(ser_request.data)
            return Response(ser_request.errors, status=status.HTTP_400_BAD_REQUEST)

        # this is serilializer save
        print(ser_request.data)
        return Response(ser_request.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
