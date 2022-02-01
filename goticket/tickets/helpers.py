# from .models import TicketCart, TicketCoupon
#
#
# class TicketCouponHelper:
#     def __init__(self):
#         self.cart_total_amount = 0
#
#     def get_coupon_discounts(self):
#         coupon_discount = TicketCoupon.objects.filter(
#             coupon_worth__lte=self.cart_total_amount
#         )
#
#         return coupon_discount
#
#
# class TicketCartHelper:
#     def __init__(self):
#         self.buyer = buyer
#         self.cart_base_total_amount = 0
#         self.cart_final_total_amount = 0
#         self.coupon_discount = 0
#         self.cart_items = []
#         self.discounts = {}
#         self.checkout_details = {"Tickets": [], "Total": [], "Amount": []}
#
#     def prepare_cart_for_checkout(self):
#         self.ticket_items = TicketCart.objects.filter(buyer=self.buyer)
#
#         if not self.ticket_items:
#             return False
#
#         self.calculate_cart_base_total_amount()
#         self.get_coupon_discount()
#         self.calculate_discount_amounts()
#         # self.get_total_amount_after_discounts()
#         self.prepare_checkout_details()
#
#         return self.checkout_details
#
#     def calculate_cart_base_total_amount(self):
#         for ticket_item in self.ticket_items:
#             self.cart_base_total_amount += (
#                 ticket_item.ticket.ticket_type.price * ticket_item.quantity
#             )
#
#     def get_total_amount_after_discounts(self):
#         coupon_helper = TicketCouponHelper
#         self.cart_final_total_amount = (
#             self.cart_base_total_amount - coupon_helper.get_coupon_discounts()
#         )
#
#         return self.cart_final_total_amount
