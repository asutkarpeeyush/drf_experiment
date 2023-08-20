from .models import Person
from django.test import TestCase

# class PersonTest(TestCase):
#     def setUp(self) -> None:
#         Person.objects.create(name="Dharmin", age=25)
#         Person.objects.create(name="Anand", age=24)

#     def assertPersonEqual(self, a: Person, b: Person) -> bool:
#         return a.name == b.name
    
#     def test_valid_person_name_age(self):
#         # Arrange
#         name = "Dharmin"
#         excepted_name_age = "Dharmin_25"

#         # Act
#         got_person = Person.objects.get(name=name)

#         # Assert
#         self.assertEqual(got_person.name_age, excepted_name_age)