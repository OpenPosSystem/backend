from timestamps.models import models
from .mixin import CardContentMixin


class Profile(CardContentMixin):
    name = models.CharField(max_length=255, verbose_name="Profile Name")
    validity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
