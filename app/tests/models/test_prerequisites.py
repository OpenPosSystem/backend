import pytest


class TestIncompatibilities:
    @pytest.mark.django_db
    def test_prerequisite_does_not_exists(self, ticket, contract):
        assert ticket.has_prerequisites([contract]) is True

    @pytest.mark.django_db
    def test_prerequisite_exists(self, prerequisite):
        assert prerequisite.primary.prerequisites == [prerequisite.secondary]
        assert prerequisite.secondary.prerequisites == []
        assert prerequisite.primary.has_prerequisites([prerequisite.secondary]) is True
        assert str(prerequisite) == f"{prerequisite.name} - {prerequisite.primary} / {prerequisite.secondary}"

    @pytest.mark.django_db
    def test_prerequisite_is_not_reversed(self, prerequisite):
        assert prerequisite.secondary.prerequisites == []
        assert prerequisite.secondary.has_prerequisites([prerequisite.primary]) is True

    @pytest.mark.django_db
    def test_prerequisite_does_not_match(self, prerequisite, ticket):
        assert prerequisite.primary.has_prerequisites([ticket]) is False

    @pytest.mark.django_db
    def test_prerequisite_multiple_value(self, prerequisite, ticket):
        assert prerequisite.primary.has_prerequisites([prerequisite.secondary, ticket]) is True

    @pytest.mark.django_db
    def test_prerequisite_multiple_value_with_all_match(self, prerequisite, ticket):
        prerequisite.primary.must_have_all_prerequisites = True
        assert prerequisite.primary.has_prerequisites([prerequisite.secondary, ticket]) is True

    @pytest.mark.django_db
    def test_prerequisite_multiple_value_with_all_match_multiple_prerequisites_ko(self, prerequisite, ticket):
        prerequisite.primary.must_have_all_prerequisites = True
        prerequisite.primary.add_prerequisite(ticket, "Model should have a ticket")
        assert prerequisite.primary.has_prerequisites([prerequisite.secondary]) is False

    @pytest.mark.django_db
    def test_prerequisite_multiple_value_with_all_match_multiple_prerequisites_ok(self, prerequisite, ticket):
        prerequisite.primary.must_have_all_prerequisites = True
        prerequisite.primary.add_prerequisite(ticket, "Model should have a ticket")
        assert prerequisite.primary.has_prerequisites([prerequisite.secondary, ticket]) is True

    @pytest.mark.django_db
    def test_prerequisite_multiple_value_with_no_name(self, contract, ticket):
        with pytest.raises(Exception) as excinfo:
            ticket.add_prerequisite(contract, None)
        assert str(excinfo.value) == "Prerequisite should have a name."

    @pytest.mark.django_db
    def test_prerequisite_multiple_value_with_invalid_model(self, user, ticket):
        with pytest.raises(Exception) as excinfo:
            ticket.add_prerequisite(user, "Model should have a user")
        assert str(excinfo.value) == f"Model {str(user)} should inherit from CardContentMixin."
