import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# Import custom manager classes
from .managers import CustomerManager, EventManagerManager, UserTypes

# from tickets.models import Ticket

"""
Custom user model inheriting from the abtract user since
there is no major Django default user settings being changed.

For reference see:
1. https://bit.ly/3zWfZ8M
2. https://bit.ly/34RB6Og
"""


class User(AbstractUser):

    # Default user type --> invoked upon registration and updated on choices
    base_type = "Super Admin"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(
        _("User Type"), max_length=13, choices=UserTypes.choices, default=base_type
    )

    """
    Save changes made to the user 'upon registration' by invoking the
    parent save method that is shipped with the Django AbstractUser class.
    """

    def save(self, *args, **kwargs):
        if not self.id:
            self.user_type = self.base_type
        return super().save(*args, **kwargs)

    class Meta:
        # app_label = 'user'
        verbose_name = "System Admin"
        verbose_name_plural = "System Admins"


class Manager(User):

    base_type = UserTypes.EVENT_MANAGER
    is_staff = True
    objects = UserManager()  # Default user manager
    active_objects = EventManagerManager()  # Custom manager

    """
    Tell Django database engine to treat this class as a proxy model.
    No table created, hence number of queries are reduced, perfomance increased
    """

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"
        proxy = True


class Customer(User):

    base_type = UserTypes.CUSTOMER

    objects = UserManager()
    active_objects = CustomerManager()

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        proxy = True


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    # tickets = models.ManyToManyField(
    # 	Ticket, on_delete=models.SET_NULL, null=True
    # )

    def __str__(self):
        return "{}'s Profile".format(self.owner.last_name)


"""
More about proxy models can be found here:
1. https://bit.ly/3Gvp7nw
2. https://bit.ly/3zVlXHa
"""
