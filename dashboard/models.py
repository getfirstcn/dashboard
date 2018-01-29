from django.db import models
from django.contrib.auth.models import User

class Server(models.Model):
    hostname = models.CharField(max_length=32, unique=True)
    ip = models.CharField(max_length=15, unique=True)
    cpu = models.CharField(max_length=50, null=True)
    mem = models.CharField(max_length=50)
    disk = models.CharField(max_length=50)
    status = models.IntegerField()
    loads = models.CharField(max_length=20)

    class Meta:
        db_table = "server"

# class test(models.Model):
#     a = models.CharField(max_length=21)
#     # on_delete = None

class IDC(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'idc'

class Department(models.Model):
    name = models.CharField(max_length=11, null=True)
    object = models.Manager()

    class Meta:
        db_table = 'department'

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    phone = models.CharField(max_length=11)
    department = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    Department = models.ForeignKey('Department',
                                   on_delete=models.CASCADE,
                                   verbose_name="department",
                                   )
    object = models.Manager()

    class Meta:
        db_table = 'user_profile'
        default_related_name = 'profile'


# Create your models here.
