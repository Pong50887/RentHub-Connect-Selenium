from django.contrib import admin

from ..models import Feature


class FeatureInline(admin.TabularInline):
    """
    Inline admin interface for adding and editing Feature objects.
    """
    model = Feature
    extra = 1  # Number of empty forms shown by default
