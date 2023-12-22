from rest_framework import serializers

from ticket.models import Ticket, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'writer')


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('uuid', 'topic', 'content', 'writer')
        depth = 1
