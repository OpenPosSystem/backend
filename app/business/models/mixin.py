from timestamps.models import models, Timestampable

from .incompatibility import Incompatibility
from .prerequisite import Prerequisite
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType


class CardContentMixin(Timestampable):
    must_have_all_prerequisites = models.BooleanField(default=False)

    @property
    def incompatibilities(self):
        content_type = ContentType.objects.get_for_model(self)

        queryset = Incompatibility.objects.filter(
            Q(
                primary_type_id=content_type.id,
                primary_id=self.id,
            )
            | Q(secondary_type_id=content_type.id, secondary_id=self.id)
        )

        return list(
            set(
                (incompatibility.primary if incompatibility.secondary == self else incompatibility.secondary)
                for incompatibility in queryset.all()
            )
        )

    @property
    def prerequisites(self):
        content_type = ContentType.objects.get_for_model(self)

        queryset = Prerequisite.objects.filter(
            primary_type_id=content_type.id,
            primary_id=self.id,
        )

        return list(set(prerequisite.secondary for prerequisite in queryset.all()))

    def has_prerequisites(self, content):
        # There is no prerequisite, we return True
        if not self.prerequisites:
            return True

        # We check that all prerequisites are matched
        if self.must_have_all_prerequisites:
            return all(prerequisite in content for prerequisite in self.prerequisites)

        # We check if at least one prerequisite is present
        return any(prerequisite in content for prerequisite in self.prerequisites)

    def add_prerequisite(self, model, name):
        if not name:
            raise Exception("Prerequisite should have a name.")
        if not isinstance(model, CardContentMixin):
            raise Exception(f"Model {model} should inherit from CardContentMixin.")

        content_type = ContentType.objects.get_for_model(self)
        model_type = ContentType.objects.get_for_model(model)

        return (
            True
            if Prerequisite.objects.create(
                name=name,
                primary_type_id=content_type.id,
                primary_id=self.id,
                secondary_type_id=model_type.id,
                secondary_id=model.id,
            )
            else False
        )

    def is_compatible_with(self, model):
        if not isinstance(model, CardContentMixin):
            raise Exception(f"Model {model} should inherit from CardContentMixin.")
        return model not in self.incompatibilities

    def set_incompatible_with(self, model, name):
        if not name:
            raise Exception("Incompatibility should have a name.")
        if not isinstance(model, CardContentMixin):
            raise Exception(f"Model {model} should inherit from CardContentMixin.")
        content_type = ContentType.objects.get_for_model(self)
        model_type = ContentType.objects.get_for_model(model)

        return (
            True
            if Incompatibility.objects.create(
                name=name,
                primary_type_id=content_type.id,
                primary_id=self.id,
                secondary_type_id=model_type.id,
                secondary_id=model.id,
            )
            else False
        )

    class Meta:
        abstract = True
