# from django.contrib.auth import get_user_model
from rest_framework import serializers

from goticket.tickets.models import TicketCart


class TicketCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCart
        fields = (
            "id",
            "ticket",
            "buyer",
            "quantity",
        )
