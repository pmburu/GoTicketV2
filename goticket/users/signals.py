# from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .managers import UserTypes
from .models import Profile

# User = get_user_model()

"""
Creating pre-save signals to set manager as staff status in Django user
"""


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def manager_to_staff_status(sender, instance, **kwargs):
    if instance is not None and instance.user_type == UserTypes.EVENT_MANAGER:
        instance.is_staff = True


"""
Signal for adding event manager to event managers group - has all permissions
"""


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_to_group(sender, instance, created, **kwargs):
    if created and instance.user_type == UserTypes.EVENT_MANAGER:
        event_managers_group = Group.objects.get(name="Event Managers")
        instance.groups.add(event_managers_group)


"""
Create user profile upon user creation
"""


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
