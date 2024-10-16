from django.contrib import admin

from ..models import Feature


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1  # Number of empty forms shown by default
