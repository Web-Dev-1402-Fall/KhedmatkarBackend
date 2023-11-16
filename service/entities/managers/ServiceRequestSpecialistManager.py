from django.db import models


class ServiceRequestSpecialistManager(models.Manager):
    def for_specialist(self, specialist):
        return self.filter(specialist=specialist)

    def first_for_request_order_by_creation(self, service_request, specialist):
        return self.filter(
            service_request=service_request,
            specialist=specialist
        ).order_by('-creation_date').first()
