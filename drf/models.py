from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

User = get_user_model()


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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
