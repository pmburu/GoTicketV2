import string
import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.crypto import get_random_string

# from goticket.users.models import User
# from goticket.events.models import Event


# Create your models here.
class TicketType(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "Ticket Type"
        verbose_name_plural = "Ticket Types"

    def __str__(self):
        return self.name


class Ticket(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    ticket_type = models.ForeignKey("tickets.TicketType", on_delete=models.CASCADE)
    number_of_tickets = models.PositiveIntegerField(default=0)
    ticket_number = ArrayField(models.CharField(max_length=6, blank=True, null=True))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("event__name", "ticket_type__name")
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return self.ticket_type.name

    # Generate ticket numbers upon ticket creation. - Randomly + secure
    def save(self, **kwargs):
        if not self.ticket_number:
            self.ticket_number = [
                get_random_string(
                    6, allowed_chars=string.ascii_uppercase + string.digits
                )
                for _ in range(self.number_of_tickets)
            ]
        return super(Ticket, self).save(**kwargs)


"""
Classes detailing ticket coupons and ticket
e.g. Best couple coupon etc. 50% coupon
"""


class TicketCoupon(models.Model):
    coupon_worth = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Coupon is Worth"
    )
    coupon_name = models.CharField(max_length=50)
    apply_to = models.ForeignKey(
        "events.Event", on_delete=models.CASCADE, related_name="event_coupon"
    )
    coupon_expiry_date = models.DateTimeField(verbose_name="Coupon Expiry", null=True)
    number_of_coupons = models.PositiveIntegerField(default=0)
    uses_per_user = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_used = models.BooleanField(default=False)
    coupon_number = ArrayField(models.CharField(max_length=6))

    def __str__(self):
        return "{0} - {1}".format(self.coupon_name, self.apply_to.name)

    # Generate coupon numbers upon save
    def save(self, **kwargs):
        if not self.coupon_number:
            self.coupon_number = [
                get_random_string(
                    6, allowed_chars=string.ascii_uppercase + string.digits
                )
                for _ in range(self.number_of_coupons)
            ]
        return super(TicketCoupon, self).save(**kwargs)

    class Meta:
        verbose_name = "Ticket Coupon"
        verbose_name_plural = "Ticket Coupons"


class TicketOrder(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ticket_orders",
    )
    paid_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    coupon = models.CharField(max_length=6)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}'s Order".format(self.buyer.last_name)

    class Meta:
        verbose_name = "Ticket Order"
        verbose_name_plural = "Ticket Orders"
        ordering = ["-date_created"]


class TicketOrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        TicketOrder, on_delete=models.CASCADE, related_name="ticket_items"
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="ticket_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "{}".format(self.id)

    class Meta:
        verbose_name = "Ticket Cart"
        verbose_name_plural = "Tickets Cart"
