from timestamps.models import models
from .mixin import CardContentMixin


class Ticket(CardContentMixin):
    name = models.CharField(max_length=255, verbose_name="Ticket Name")
    price = models.PositiveIntegerField(default=0)
    entries = models.PositiveIntegerField(default=1)
    validity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
