from django.db import models

# Create your models here.

from service.entities import ServiceRequest
from service.entities import ServiceRequestSpecialist
from service.entities import Specialty


class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
