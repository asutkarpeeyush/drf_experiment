from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    # Lets consider this as a Student/Employee
    class Meta:
        db_table = "person"
        ordering = ['age']

    subject_choices = [
        ('EN', 'ENGLISH'),
        ('HN', 'HINDI'),
        ('MT', 'MATHS')
    ]

    # class variables
    name = models.CharField(max_length=20, unique=True)
    age = models.IntegerField(null=True)
    address = models.TextField(max_length=200, default='')
    subject = models.CharField(
        choices=subject_choices, max_length=2, null=True)
    updated_by = models.ForeignKey(User, related_name='people',
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + " " + str(self.age) + " " + str(self.subject)

    @property
    def name_age(self):
        return self.name + "_" + str(self.age)
