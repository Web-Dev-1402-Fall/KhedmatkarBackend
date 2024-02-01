from django.db import models
from service.entities import ServiceRequestStatus, ServiceRequestSpecialistStatus
from user.models import Customer, Specialist
# Create your models here.


class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class ServiceRequest(models.Model):
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    reception_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    accepted_specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add a default value
    status = models.CharField(
        max_length=50,
        choices=ServiceRequestStatus.ServiceRequestStatus.choices,  # Use .choices here
        default=ServiceRequestStatus.ServiceRequestStatus.FINDING_SPECIALIST,
    )


class ServiceRequestSpecialist(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, null=True)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, null=True)
    status = models.CharField(
        max_length=50,
        choices=ServiceRequestSpecialistStatus.ServiceRequestSpecialistStatus.choices,
        # Correct if ServiceRequestSpecialistStatus is a TextChoices subclass
    )
