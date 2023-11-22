from django.db import models
from service.entities import ServiceRequestSpecialistStatus
from service.entities.ServiceRequest import ServiceRequest
from user.models import Specialist


class ServiceRequestSpecialist(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, null=True)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, null=True)
    status = models.CharField(
        max_length=50,
        choices=ServiceRequestSpecialistStatus.ServiceRequestSpecialistStatus.choices,
        # Correct if ServiceRequestSpecialistStatus is a TextChoices subclass
    )
