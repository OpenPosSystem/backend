from timestamps.models import models, Timestampable
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Prerequisite(Timestampable):
    name = models.CharField(max_length=255, verbose_name="Prerequisite")

    primary_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="primary_prerequisites")
    primary_id = models.PositiveIntegerField()
    primary = GenericForeignKey("primary_type", "primary_id")

    secondary_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="secondary_prerequisites")
    secondary_id = models.PositiveIntegerField()
    secondary = GenericForeignKey("secondary_type", "secondary_id")

    def __str__(self):
        return f"{self.name} - {self.primary} / {self.secondary}"
