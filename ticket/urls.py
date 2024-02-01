from django.urls import path
from ticket.views import *

urlpatterns = [
    path('create/', CreateTicketView.as_view()),
    path('list/', TicketListView.as_view()),
    path('details/', TicketDetailView.as_view()),
]
