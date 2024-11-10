from django.db import models


class Announcement(models.Model):
    """
    Represents an announcement for the tenants.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=500)
    publish_date = models.DateTimeField()

    def __str__(self):
        """Returns the string representation of the announcement, which is its title."""
        return self.title
