from django.db import models


class ServiceRequestStatus(models.TextChoices):
    FINDING_SPECIALIST = 'FINDING_SPECIALIST', 'Finding Specialist'
    WAITING_FOR_SPECIALIST_ACCEPTANCE = 'WAITING_FOR_SPECIALIST_ACCEPTANCE', 'Waiting for Specialist Acceptance'
    WAITING_FOR_CUSTOMER_ACCEPTANCE = 'WAITING_FOR_CUSTOMER_ACCEPTANCE', 'Waiting for Customer Acceptance'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    DONE = 'DONE', 'Done'
    CANCELED = 'CANCELED', 'Canceled'
