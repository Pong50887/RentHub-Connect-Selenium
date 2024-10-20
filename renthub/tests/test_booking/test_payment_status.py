"""Tests of booking: payment status."""

from django.test import TestCase
from django.urls import reverse
from renthub.models import Rental, Room, Renter
