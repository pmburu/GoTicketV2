from django.contrib import admin

from .models import Ticket, TicketCoupon, TicketType


# Register your models here.
@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "event", "price")
    list_editable = ("price",)
    search_fields = (
        "name",
        "event",
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("event", "ticket_type", "date_created", "number_of_tickets")
    readonly_fields = ("ticket_number",)

    search_fields = ("event", "ticket_type")


@admin.register(TicketCoupon)
class TicketCouponAdmin(admin.ModelAdmin):
    list_display = ("coupon_worth", "coupon_name", "apply_to", "number_of_coupons")
    readonly_fields = ("coupon_number",)

    search_fields = ("ticket", "buyer")

    list_per_page = 25

    # def has_add_permission(self, request):
    #     return False
