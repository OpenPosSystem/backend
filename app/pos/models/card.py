from django.contrib.contenttypes.models import ContentType
from timestamps.models import models, Timestampable
from datetime import datetime, timedelta
from django.utils import timezone
from business.models import Contract, Ticket
from django.db.models import Q, Case, When, IntegerField
from django.conf import settings


def get_current_timestamp():
    return timezone.make_aware(datetime.now(), timezone.get_current_timezone())


class CardContentAddException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Card(Timestampable):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="cards",
    )
    uid = models.CharField(max_length=14, unique=True, verbose_name="Card UID")

    def __str__(self):
        return self.uid

    INCOMPATIBLE_CONTENT_TYPES = [
        ("contract", "ticket"),
        ("contract", "contract"),
        ("profile", "profile"),
    ]

    def contains_type(self, content_type):
        return any(ContentType.objects.get_for_model(content).model == content_type for content in self.contents)

    def raise_content_exception(self, content):
        # We verify that the card contents don't have any incompatibility with the new content we wish to add
        for existing_content in self.contents:
            if not existing_content.is_compatible_with(content):
                raise CardContentAddException(f"Content {existing_content} is not compatible with {content}.")

        # We verify that the content we wish to add match all prerequisites of the card
        if not content.has_prerequisites(self.contents):
            raise CardContentAddException(
                f"Cannot add {content} because the card does not have required prerequisites."
            )

        # We verify that the card content is compatible with the content we wish to add
        content_type = ContentType.objects.get_for_model(content).model
        for content_type_a, content_type_b in self.INCOMPATIBLE_CONTENT_TYPES:
            if content_type == content_type_a and self.contains_type(content_type_b):
                raise CardContentAddException(
                    f"Cannot add a {content_type_a} because the card already has a {content_type_b}."
                )

    def can_add_content(self, content):
        try:
            self.raise_content_exception(content)
            return True
        except CardContentAddException:
            return False

    def add_content(self, content):
        from .card_content import CardContent

        if content in self.contents:
            return
        self.raise_content_exception(content)
        CardContent.objects.create(
            card=self,
            content_type=ContentType.objects.get_for_model(content),
            object_id=content.id,
            expires_at=get_current_timestamp() + timedelta(seconds=content.validity),
            price=getattr(content, "price", None),
        )

    def get_content_to_use(self):
        current_timestamp = get_current_timestamp()
        contract_type = ContentType.objects.get_for_model(Contract)
        ticket_type = ContentType.objects.get_for_model(Ticket)

        queryset = (
            self.card_contents.filter(expires_at__gt=current_timestamp)
            .filter(Q(content_type=contract_type) | Q(content_type=ticket_type))
            .annotate(
                contracts_first=Case(
                    When(content_type=contract_type, then=1),
                    When(content_type=ticket_type, then=2),
                    output_field=IntegerField(),
                )
            )
            .order_by("contracts_first", "expires_at", "id")
        )

        return queryset.first()

    @property
    def contents(self):
        content_queryset = self.card_contents.filter(expires_at__gt=get_current_timestamp())
        return [content.content_object for content in content_queryset.all()]
