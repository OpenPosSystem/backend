from timestamps.models import models
from .mixin import CardContentMixin


class Contract(CardContentMixin):
    name = models.CharField(max_length=255, verbose_name="Contract Name")
    price = models.PositiveIntegerField(default=0)
    turnstile_timer = models.PositiveIntegerField(default=3600)
    validity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
