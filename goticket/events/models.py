import uuid
from pathlib import Path

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from star_ratings.models import Rating

"""Upload helper function - to save image as id - filename"""


def image_upload(instance, filename):
    path = Path(filename)
    return "event/{}{}".format(uuid.uuid4(), path.suffix)


# Create your models here.
class Event(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=4000)
    location = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to=image_upload)
    background_image = models.ImageField(upload_to=image_upload)
    time = models.DateTimeField()
    manager = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="event_manager"
    )
    active = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name


class Attendance(models.Model):
    """
    A class to handle only customers atteding / bought tickets for this event.
    Helps managers only view their 'customers' and not other users 'customers'
    in the system.

    When an event is deleted, the attendee should not be deleted.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(
        "events.Event", on_delete=models.CASCADE, related_name="my_event"
    )
    attendee = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="attending"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.attendee.last_name

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"


class Comments(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField(max_length=4000)
    rating = GenericRelation(Rating, related_query_name="comment_rating")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="attendee_comments",
    )
    event = models.ForeignKey(
        "events.Event", on_delete=models.CASCADE, related_name="event_comments"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return "%s's comment on s% event" % (self.user.last_name, self.event.name)
