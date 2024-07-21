import pytest as pytest

from business.models import Contract, Ticket, Profile
from pos.models import Card, CardContent
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_contract(contract):
    assert isinstance(contract, Contract)
    assert contract.name
    assert contract.price >= 100
    assert contract.price <= 10000
    assert contract.turnstile_timer >= 1
    assert contract.turnstile_timer <= 60
    assert str(contract) == contract.name
    assert contract.must_have_all_prerequisites is False


@pytest.mark.django_db
def test_create_ticket(ticket):
    assert isinstance(ticket, Ticket)
    assert ticket.name
    assert ticket.price >= 10
    assert ticket.price <= 500
    assert str(ticket) == ticket.name
    assert ticket.must_have_all_prerequisites is False


@pytest.mark.django_db
def test_create_profile(profile):
    assert isinstance(profile, Profile)
    assert profile.name
    assert str(profile) == profile.name
    assert profile.must_have_all_prerequisites is False


@pytest.mark.django_db
def test_create_card(card):
    assert isinstance(card, Card)
    assert card.uid
    assert str(card) == card.uid


@pytest.mark.django_db
def test_create_card_content_contract(card_content_contract):
    assert isinstance(card_content_contract, CardContent)
    assert card_content_contract.content_type.model == "contract"
    assert (
        str(card_content_contract) == f"{card_content_contract.content_type} - {card_content_contract.content_object}"
    )


@pytest.mark.django_db
def test_create_card_content_ticket(card_content_ticket):
    assert isinstance(card_content_ticket, CardContent)
    assert card_content_ticket.content_type.model == "ticket"
    assert str(card_content_ticket) == f"{card_content_ticket.content_type} - {card_content_ticket.content_object}"


@pytest.mark.django_db
def test_create_card_content_profile(card_content_profile):
    assert isinstance(card_content_profile, CardContent)
    assert card_content_profile.content_type.model == "profile"
    assert str(card_content_profile) == f"{card_content_profile.content_type} - {card_content_profile.content_object}"


@pytest.mark.django_db
def test_create_superuser():
    User = get_user_model()
    email = "superuser@example.com"
    password = "supersecretpassword"

    extra_fields = {
        "is_staff": True,
        "is_superuser": True,
        "first_name": "Super",
        "last_name": "User",
    }

    user = User.objects.create_superuser(email=email, password=password, **extra_fields)

    assert user.email == email
    assert user.is_staff
    assert user.is_superuser
    assert user.check_password(password) is True
    assert user.first_name == "Super"
    assert user.last_name == "User"
    assert str(user) == email


@pytest.mark.django_db
def test_create_superuser_without_email():
    User = get_user_model()
    password = "supersecretpassword"

    with pytest.raises(ValueError) as excinfo:
        User.objects.create_superuser(email=None, password=password)
    assert str(excinfo.value) == "The Email field must be set"


@pytest.mark.django_db
def test_create_superuser_without_staff_raises_exception():
    User = get_user_model()
    password = "supersecretpassword"

    extra_fields = {
        "is_staff": False,
        "is_superuser": True,
        "first_name": "Super",
        "last_name": "User",
    }

    with pytest.raises(ValueError) as excinfo:
        User.objects.create_superuser(email=None, password=password, **extra_fields)
    assert str(excinfo.value) == "Superuser must have is_staff=True."


@pytest.mark.django_db
def test_create_superuser_without_superuser_raises_exception():
    User = get_user_model()
    password = "supersecretpassword"

    extra_fields = {
        "is_staff": True,
        "is_superuser": False,
        "first_name": "Super",
        "last_name": "User",
    }

    with pytest.raises(ValueError) as excinfo:
        User.objects.create_superuser(email=None, password=password, **extra_fields)
    assert str(excinfo.value) == "Superuser must have is_superuser=True."


@pytest.mark.django_db
def test_create_user_with_superadmin_privilege():
    User = get_user_model()
    email = "superuser@example.com"
    password = "supersecretpassword"

    extra_fields = {
        "is_staff": True,
        "is_superuser": True,
        "first_name": "Super",
        "last_name": "User",
    }

    user = User.objects.create_user(email=email, password=password, **extra_fields)

    assert user.email == email
    assert user.is_staff
    assert user.is_superuser
    assert user.check_password(password) is True
    assert user.first_name == "Super"
    assert user.last_name == "User"


@pytest.mark.django_db
def test_create_user_with_staff_privilege():
    User = get_user_model()
    email = "superuser@example.com"
    password = "supersecretpassword"

    extra_fields = {
        "is_staff": True,
        "is_superuser": False,
        "first_name": "Super",
        "last_name": "User",
    }

    user = User.objects.create_user(email=email, password=password, **extra_fields)

    assert user.email == email
    assert user.is_staff
    assert not user.is_superuser
    assert user.check_password(password) is True
    assert user.first_name == "Super"
    assert user.last_name == "User"


@pytest.mark.django_db
def test_create_user():
    User = get_user_model()
    email = "superuser@example.com"
    password = "supersecretpassword"

    extra_fields = {
        "is_staff": False,
        "is_superuser": False,
        "first_name": "Super",
        "last_name": "User",
    }

    user = User.objects.create_user(email=email, password=password, **extra_fields)

    assert user.email == email
    assert not user.is_staff
    assert not user.is_superuser
    assert user.check_password(password) is True
    assert user.first_name == "Super"
    assert user.last_name == "User"


@pytest.mark.django_db
def test_update_user(user):
    user.password = "toto"
    user.save()
    assert user.password != "toto"
    assert user.check_password("toto") is True
