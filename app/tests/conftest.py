import pytest
from .factories import (
    UserFactory,
    ContractFactory,
    TicketFactory,
    ProfileFactory,
    CardFactory,
    CardContentTicketFactory,
    CardContentContractFactory,
    CardContentProfileFactory,
    IncompatibilityFactory,
    PrerequisiteFactory,
    AdminUserFactory,
)
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture()
def user(db):
    return UserFactory()


@pytest.fixture
def admin_user(db):
    return AdminUserFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    def _authenticate(user):
        token = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        return api_client

    yield _authenticate
    api_client.credentials()


@pytest.fixture
def authenticated_user_client(user, authenticated_client):
    return authenticated_client(user)


@pytest.fixture
def authenticated_admin_client(admin_user, authenticated_client):
    return authenticated_client(admin_user)


@pytest.fixture
def contract():
    return ContractFactory()


@pytest.fixture
def ticket():
    return TicketFactory()


@pytest.fixture
def profile():
    return ProfileFactory()


@pytest.fixture
def card():
    return CardFactory()


@pytest.fixture
def card_user(user):
    return CardFactory(user=user)


@pytest.fixture
def card_content_contract():
    return CardContentContractFactory()


@pytest.fixture
def card_content_ticket():
    return CardContentTicketFactory()


@pytest.fixture
def card_content_profile():
    return CardContentProfileFactory()


@pytest.fixture
def incompatibility():
    return IncompatibilityFactory()


@pytest.fixture
def prerequisite():
    return PrerequisiteFactory()
