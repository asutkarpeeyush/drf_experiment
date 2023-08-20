from rest_framework.test import APITestCase
from .models import Person
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class PersonAPITest(APITestCase):
    def setUp(self) -> None:
        Person.objects.create(name="Dharmin", age=25)
        Person.objects.create(name="Anand", age=24)

        # authenticate the user
        user = User.objects.create(username="piyush", password="piyush")
        self.client.force_login(user=user)
        

    def test_get_person_details(self):
        # arrange
        url = reverse('v1:details-list')
        num_of_entries = 2

        # act 
        response = self.client.get(url, {})

        # assert
        # print(response.data.get('results', []))
        results = response.data.get('results', [])
        self.assertEqual(len(results), num_of_entries)
        self.assertEqual(results[0].get('name'), 'Anand')
        self.assertEqual(results[1].get('name'), 'Dharmin')


    def test_get_individual_details(self):
        # arrange
        url = reverse('v1:details-detail', args=[str(1)])
        num_of_entries = 1

        # act
        response = self.client.get(url)

        # assert
        result = response.data
        self.assertEqual(result.get('name', ""), "Dharmin")
