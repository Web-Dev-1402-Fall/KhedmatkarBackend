from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ticket.models import Ticket, Comment
from ticket.serializers import TicketSerializer, CommentSerializer


# Create your views here.
class CreateTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        if user.is_admin is False:
            ticket = Ticket.objects.create(writer=user, content=data['content'], topic=data['topic'])
            ticket.save()
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": "You can't create a ticket"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TicketListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.filter(writer=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ticket = Ticket.objects.filter(uuid=request.query_params.get('uuid', '')).first()
        if ticket is None:
            return Response({'message': 'Ticket does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(ticket=ticket)
        serializer = CommentSerializer(comments, many=True)
        return Response(data={**TicketSerializer(ticket).data, "comments": serializer.data}, status=status.HTTP_200_OK)
