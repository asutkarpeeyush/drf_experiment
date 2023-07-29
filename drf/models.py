from django.db import models


class Person(models.Model):
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

    def __str__(self):
        return self.name + " " + str(self.age) + " " + str(self.subject)

    @property
    def name_age(self):
        return self.name + "_" + str(self.age)
