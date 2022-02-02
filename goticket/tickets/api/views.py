from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from goticket.tickets.models import TicketCoupon, TicketOrder

from .serializers import MyTicketOrderSerializer, TicketOrderSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = TicketOrder.objects.all()
    serializer_class = MyTicketOrderSerializer
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self, request):
    #     me = self.request.user
    #     qs = TicketOrder.objects.filter(buyer=me)
    #
    #     return qs

    @action(methods="POST", detail=False, url_path="checkout/", url_name="checkout")
    def checkout(self, request, *args, **kwargs):

        serializer = TicketOrderSerializer

        if serializer.is_valid:
            amount_owed = sum(
                ticket_item.get("quantity") * ticket_item.get("ticket").price
                for ticket_item in serializer.validated_data["ticket_items"]
            )

            try:
                now = timezone.now()
                code = list(TicketCoupon.objects.values_list("coupon_name", flat=True))
                coupon = TicketCoupon.objects.filter(
                    coupon_number__contains=code,
                    date_created__lte=now,
                    coupon_expiry_date__gte=now,
                    active=True,
                    is_used=False,
                )
                if coupon:
                    try:
                        # Create a list of the event from customer's cart
                        current_event = list(
                            ticket_item.get("ticket").event
                            for ticket_item in serializer.validated_data["ticket_items"]
                        )

                        # Create a list of events from filtered coupon queryset
                        event_in_coupon = coupon.values_list("event", flat=True)

                        # Check whether coupon matches event - being purchased
                        # i.e. if what the user is purchasing has a coupon
                        if set(current_event).intersection(event_in_coupon):

                            coupon_deductions = coupon.coupon_worth - amount_owed
                            serializer.save(
                                buyer=request.user,
                                paid_amount=coupon_deductions,
                                coupon=coupon,
                            )

                            coupon.is_used = True
                            coupon.save()

                            return Response(
                                serializer.data, status=status.HTTP_201_CREATED
                            )
                        return Response(
                            "Coupon not for the event you are trying to purchase tickets"
                        )
                    except Exception as e:
                        return Response(
                            serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                            data={"Error": str(e)},
                        )
                return Response("Coupons expired or used")
            except Exception as e:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"Error": str(e)},
                )
        return Response("Invalid Serializer")
