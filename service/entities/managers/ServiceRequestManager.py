from django.db import models
from django.utils import timezone


class ServiceRequestManager(models.Manager):
    def for_customer(self, customer):
        return self.filter(customer=customer)

    def for_customer_after_date_with_address(self, customer, date, address_keyword):
        return self.filter(
            customer=customer,
            creation_date__gte=date,
            address__icontains=address_keyword
        )
