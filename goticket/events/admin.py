from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Attendance, Comments, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    ordering = ["date_created"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Filter only the events created by this manager
        if not request.user.is_superuser:
            me = request.user.pk
            return qs.filter(manager=me)

        # Else show all events to superuser
        return qs

    # Functions to autoselect current logged in manager during event creation
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "manager":
            kwargs["queryset"] = get_user_model().objects.filter(
                username=request.user.username
            )
        return super(EventAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + [
                "manager",
            ]
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data["manager"] = request.user
        request.GET = data
        return super(EventAdmin, self).add_view(
            request, form_url="", extra_context=extra_context
        )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("attendee", "event")


# Register your models here.
admin.site.register(Comments)
