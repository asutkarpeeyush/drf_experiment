from django.urls import path
from . import views


urlpatterns = [
    path('details', views.person_details, name='my_app_details')
]
