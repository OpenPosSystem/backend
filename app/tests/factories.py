import random

import factory
from pytest_factoryboy import register
from business.models import Contract, Ticket, Profile, Incompatibility, Prerequisite
from pos.models import Card, CardContent
from faker import Faker
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from factory.django import DjangoModelFactory
from django.contrib.auth.hashers import make_password

faker = Faker()
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: faker.user_name())
    email = factory.LazyAttribute(lambda x: faker.email())
    password = factory.LazyFunction(lambda: make_password("password"))  # Hashes the password directly


class AdminUserFactory(UserFactory):
    is_staff = True
    is_superuser = True


@register
class ContractFactory(DjangoModelFactory):
    class Meta:
        model = Contract

    name = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    price = factory.LazyAttribute(lambda x: faker.random_int(min=100, max=10000))
    turnstile_timer = factory.LazyAttribute(lambda x: faker.random_int(min=1, max=60))
    validity = factory.LazyAttribute(lambda x: faker.random_int(min=60, max=6000))


@register
class TicketFactory(DjangoModelFactory):
    class Meta:
        model = Ticket

    name = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    price = factory.LazyAttribute(lambda x: faker.random_int(min=10, max=500))
    validity = factory.LazyAttribute(lambda x: faker.random_int(min=60, max=6000))


@register
class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    name = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    validity = factory.LazyAttribute(lambda x: faker.random_int(min=60, max=6000))


@register
class CardFactory(DjangoModelFactory):
    class Meta:
        model = Card

    user = factory.SubFactory(UserFactory)
    uid = factory.LazyFunction(lambda: faker.unique.bothify(text="########??????"))


@register
class CardContentContractFactory(DjangoModelFactory):
    class Meta:
        model = CardContent

    card = factory.SubFactory(CardFactory)
    content_type = factory.LazyAttribute(lambda x: ContentType.objects.get_for_model(Contract))
    object_id = factory.LazyAttribute(lambda x: ContractFactory().id)
    expires_at = factory.LazyAttribute(lambda x: faker.future_datetime())
    price = factory.LazyAttribute(lambda x: faker.random_int(min=100, max=10000))


@register
class CardContentTicketFactory(DjangoModelFactory):
    class Meta:
        model = CardContent

    card = factory.SubFactory(CardFactory)
    content_type = factory.LazyAttribute(lambda x: ContentType.objects.get_for_model(Ticket))
    object_id = factory.LazyAttribute(lambda x: TicketFactory().id)
    expires_at = factory.LazyAttribute(lambda x: faker.future_datetime())
    price = factory.LazyAttribute(lambda x: faker.random_int(min=100, max=10000))


@register
class CardContentProfileFactory(DjangoModelFactory):
    class Meta:
        model = CardContent

    card = factory.SubFactory(CardFactory)
    content_type = factory.LazyAttribute(lambda x: ContentType.objects.get_for_model(Profile))
    object_id = factory.LazyAttribute(lambda x: ProfileFactory().id)
    expires_at = factory.LazyAttribute(lambda x: faker.future_datetime())
    price = factory.LazyAttribute(lambda x: faker.random_int(min=100, max=10000))


@register
class IncompatibilityFactory(DjangoModelFactory):
    class Meta:
        model = Incompatibility

    name = factory.Faker("sentence", nb_words=4)

    @factory.lazy_attribute
    def primary(self):
        primary_factory = random.choice([ContractFactory, TicketFactory, ProfileFactory])
        return primary_factory()

    @factory.lazy_attribute
    def primary_type(self):
        return ContentType.objects.get_for_model(self.primary)

    @factory.lazy_attribute
    def primary_id(self):
        return self.primary.id

    @factory.lazy_attribute
    def secondary(self):
        secondary_factory = random.choice([ContractFactory, TicketFactory, ProfileFactory])
        return secondary_factory()

    @factory.lazy_attribute
    def secondary_type(self):
        return ContentType.objects.get_for_model(self.secondary)

    @factory.lazy_attribute
    def secondary_id(self):
        return self.secondary.id


@register
class PrerequisiteFactory(DjangoModelFactory):
    class Meta:
        model = Prerequisite

    name = factory.Faker("sentence", nb_words=4)

    @factory.lazy_attribute
    def primary(self):
        primary_factory = random.choice([TicketFactory, ProfileFactory])
        return primary_factory()

    @factory.lazy_attribute
    def primary_type(self):
        return ContentType.objects.get_for_model(self.primary)

    @factory.lazy_attribute
    def primary_id(self):
        return self.primary.id

    @factory.lazy_attribute
    def secondary(self):
        secondary_factory = random.choice([TicketFactory])
        return secondary_factory()

    @factory.lazy_attribute
    def secondary_type(self):
        return ContentType.objects.get_for_model(self.secondary)

    @factory.lazy_attribute
    def secondary_id(self):
        return self.secondary.id
