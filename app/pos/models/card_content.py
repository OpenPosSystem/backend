from timestamps.models import models, Timestampable
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .card import Card


class CardContent(Timestampable):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="card_contents")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    expires_at = models.DateTimeField(null=True)
    price = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.content_type} - {self.content_object}"
