from django.db import models


# Create your models here.

class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


from django.db import models


class Specialty(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


from django.db import models
from django.db.models import JSONField
from service.entities import ServiceRequestStatus
from user.models import Customer, Specialist


class ServiceRequest(models.Model):
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    reception_date = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    accepted_specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=ServiceRequestStatus.ServiceRequestStatus.choices,  # Use .choices here
        default=ServiceRequestStatus.ServiceRequestStatus.FINDING_SPECIALIST,
    )


from django.db import models
from service.entities import ServiceRequestSpecialistStatus
from user.models import Specialist


class ServiceRequestSpecialist(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, null=True)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, null=True)
    status = models.CharField(
        max_length=50,
        choices=ServiceRequestSpecialistStatus.ServiceRequestSpecialistStatus.choices,
        # Correct if ServiceRequestSpecialistStatus is a TextChoices subclass
    )
