from rest_framework import serializers

from goticket.tickets.models import Ticket, TicketOrder, TicketOrderItem


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "event", "ticket_type", "number_of_tickets", "ticket_number")


class MyTicketOrderItemSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer()

    class Meta:
        model = TicketOrderItem
        fields = ("ticket", "quantity", "total")


class MyTicketOrderSerializer(serializers.ModelSerializer):
    tickets = MyTicketOrderItemSerializer(many=True)

    class Meta:
        model = TicketOrder
        fields = ("id", "buyer", "tickets", "coupon")


class TicketOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketOrderItem
        fields = ("ticket", "quantity", "total")


class TicketOrderSerializer(serializers.ModelSerializer):
    ticket_items = TicketOrderItemSerializer(many=True)

    class Meta:
        model = TicketOrder
        fields = ("id", "buyer", "ticket_items", "coupon")

    def create(self, validated_data):
        ticket_items_data = validated_data.pop("ticket_items")
        ticket_order = TicketOrder.objects.create(**validated_data)

        for ticket_item_data in ticket_items_data:
            TicketOrderItem.objects.create(order=ticket_order, **ticket_item_data)
        return ticket_order
