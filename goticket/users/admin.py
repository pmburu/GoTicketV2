from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .managers import UserTypes
from .models import Customer, Manager

# from events.models import Event, Attendance

User = get_user_model()


@admin.register(Manager)
class ManagerAdmin(UserAdmin):
    fieldsets = (
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "groups",
                )
            },
        ),
        (_("User Type"), {"fields": ("user_type",)}),
        (_("Access Credentials"), {"fields": ("username", "password")}),
    )
    search_fields = ("username__startswith",)
    list_display = [
        "username",
        "email",
        "last_name",
        "user_type",
        "is_staff",
        "is_active",
        "last_login",
    ]
    list_per_page = 25

    # Filter only Event Managers
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            me = request.user.pk
            return qs.filter(Q(user_type=UserTypes.EVENT_MANAGER) & Q(pk=me))
        return qs.filter(user_type=UserTypes.EVENT_MANAGER)


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    fieldsets = (
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Permissions"), {"fields": ("groups",)}),
        (_("User Type"), {"fields": ("user_type",)}),
        (_("Access Credentials"), {"fields": ("username", "password")}),
    )
    readonly_fields = ["user_type"]
    search_fields = ("username__startswith",)
    list_display = [
        "username",
        "email",
        "last_name",
        "user_type",
        "is_active",
        "last_login",
    ]

    list_per_page = 25

    # Filter only Customers
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            """
            Filter by attendance to my event where user
            is attending and is customer and the event is organized by
            me.
            """
            customer = qs.filter(user_type=UserTypes.CUSTOMER)
            # Some logic here
            return customer
        return qs.filter(user_type=UserTypes.CUSTOMER)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "last_name",
        "base_type",
        "is_superuser",
        "is_active",
        "last_login",
    ]

    # Filter only Customers
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=True)
