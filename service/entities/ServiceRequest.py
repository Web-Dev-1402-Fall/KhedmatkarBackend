from django.db import models
from django.db.models import JSONField
from service.entities import ServiceRequestStatus
from service.entities.Specialty import Specialty
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
    geo_point = JSONField()
