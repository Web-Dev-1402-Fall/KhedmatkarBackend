import uuid
from django.db import models
from user.models import User


class Ticket(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=250)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
