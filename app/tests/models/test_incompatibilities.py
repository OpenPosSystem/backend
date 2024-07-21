import pytest
from business.models import Incompatibility


class TestIncompatibilities:
    @pytest.mark.django_db
    def test_incompatibility_with_two_models(self, ticket, contract):
        assert ticket.is_compatible_with(contract) is True

    @pytest.mark.django_db
    def test_incompatibility_with_two_models_ko(self, incompatibility):
        assert incompatibility.primary.is_compatible_with(incompatibility.secondary) is False
        assert incompatibility.secondary.is_compatible_with(incompatibility.primary) is False
        assert (
            str(incompatibility)
            == f"{incompatibility.name} - {incompatibility.primary.name} / {incompatibility.secondary.name}"
        )

    @pytest.mark.django_db
    def test_incompatibility_creation(self, ticket, contract):
        assert Incompatibility.objects.count() == 0
        assert ticket.is_compatible_with(contract) is True
        ticket.set_incompatible_with(contract, "Testing incompatibility")
        assert Incompatibility.objects.count() == 1
        incompatibility = Incompatibility.objects.first()
        assert incompatibility.name == "Testing incompatibility"
        assert incompatibility.primary == ticket
        assert incompatibility.secondary == contract
        assert ticket.is_compatible_with(contract) is False

    @pytest.mark.django_db
    def test_incompatibility_creation_without_name(self, ticket, contract):
        with pytest.raises(Exception) as excinfo:
            ticket.set_incompatible_with(contract, None)
        assert str(excinfo.value) == "Incompatibility should have a name."

    @pytest.mark.django_db
    def test_incompatibility_creation_with_invalid_nodel(self, ticket, user):
        with pytest.raises(Exception) as excinfo:
            ticket.set_incompatible_with(user, "Testing incompatibility")
        assert str(excinfo.value) == f"Model {str(user)} should inherit from CardContentMixin."

    @pytest.mark.django_db
    def test_incompatibility(self, incompatibility):
        assert incompatibility.primary.is_compatible_with(incompatibility.secondary) is False

    @pytest.mark.django_db
    def test_incompatibility_with_invalid_model(self, ticket, user):
        with pytest.raises(Exception) as excinfo:
            assert ticket.is_compatible_with(user) is False
        assert str(excinfo.value) == f"Model {str(user)} should inherit from CardContentMixin."
