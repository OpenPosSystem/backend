import pytest
from freezegun import freeze_time
from pos.models.card import CardContentAddException
from ..factories import ContractFactory, TicketFactory


class TestCardContent:

    @pytest.mark.django_db
    @freeze_time("2012-01-14")
    def test_add_card_content(self, card, contract):
        assert card.contents == []
        card.add_content(contract)
        assert card.contents == [contract]

    @pytest.mark.django_db
    def test_add_card_content_validity(self, card, contract):
        assert card.contents == []
        with freeze_time("2012-01-14"):
            card.add_content(contract)
            card_content = card.card_contents.first()
            assert card_content.content_object == contract
            validity = card_content.expires_at - card_content.created_at
            assert validity.total_seconds() == contract.validity

    @pytest.mark.django_db
    def test_add_card_ticket_after_contract_works(self, card, contract, ticket):
        assert card.contents == []
        with freeze_time("2012-01-14"):
            card.add_content(contract)
            card.add_content(ticket)
            assert card.contents == [contract, ticket]

    @pytest.mark.django_db
    def test_add_card_contract_after_ticket_raises_error(self, card, contract, ticket):
        assert card.contents == []
        with freeze_time("2012-01-14"):
            card.add_content(ticket)
            with pytest.raises(CardContentAddException) as excinfo:
                card.add_content(contract)
            assert str(excinfo.value) == "Cannot add a contract because the card already has a ticket."

    @pytest.mark.django_db
    def test_add_contract_after_contract_raises_error(self, card, contract, ticket):
        assert card.contents == []
        new_contract = ContractFactory()
        with freeze_time("2012-01-14"):
            card.add_content(contract)
            with pytest.raises(CardContentAddException) as excinfo:
                card.add_content(new_contract)
            assert str(excinfo.value) == "Cannot add a contract because the card already has a contract."

    @pytest.mark.django_db
    def test_add_contract_duplicate_is_ignored(self, card, contract, ticket):
        assert card.contents == []
        with freeze_time("2012-01-14"):
            card.add_content(contract)
            card.add_content(contract)
            assert card.contents == [contract]

    @pytest.mark.django_db
    def test_add_contract_after_expired_contract(self, card, contract, ticket):
        assert card.contents == []
        new_contract = ContractFactory()

        with freeze_time("2012-01-14") as frozen_time:
            card.add_content(contract)
            assert card.contents == [contract]
            frozen_time.tick(delta=contract.validity)
            card.add_content(new_contract)
            assert card.contents == [new_contract]

    @pytest.mark.django_db
    def test_add_ticket_after_expired_contract(self, card, contract, ticket):
        assert card.contents == []

        with freeze_time("2012-01-14") as frozen_time:
            card.add_content(ticket)
            assert card.contents == [ticket]
            frozen_time.tick(delta=ticket.validity)
            card.add_content(contract)
            assert card.contents == [contract]

    @pytest.mark.django_db
    def test_add_ticket_after_ticket(self, card, ticket):
        assert card.contents == []
        new_ticket = TicketFactory()

        with freeze_time("2012-01-14"):
            card.add_content(ticket)
            assert card.contents == [ticket]
            assert card.can_add_content(new_ticket) is True
            card.add_content(new_ticket)
            assert card.contents == [ticket, new_ticket]

    @pytest.mark.django_db
    def test_add_card_contract_incompatible(self, card, incompatibility):
        assert card.contents == []
        with freeze_time("2012-01-14"):
            card.add_content(incompatibility.primary)
            assert card.can_add_content(incompatibility.secondary) is False
            with pytest.raises(CardContentAddException) as excinfo:
                card.add_content(incompatibility.secondary)
            assert (
                str(excinfo.value)
                == f"Content {incompatibility.primary.name} is not compatible with {incompatibility.secondary.name}."
            )

    @pytest.mark.django_db
    def test_add_card_without_prerequisites(self, card, prerequisite):
        assert card.contents == []
        with freeze_time("2012-01-14"):
            with pytest.raises(CardContentAddException) as excinfo:
                card.add_content(prerequisite.primary)
            assert (
                str(excinfo.value)
                == f"Cannot add {prerequisite.primary.name} because the card does not have required prerequisites."
            )

    @pytest.mark.django_db
    def test_add_card_without_all_prerequisites(self, card, profile, ticket, prerequisite):
        assert card.contents == []
        new_ticket = TicketFactory()
        ticket.add_prerequisite(profile, "Require profile")
        ticket.add_prerequisite(new_ticket, "Require ticket")
        assert card.contents == []
        with freeze_time("2012-01-14"):
            card.add_content(profile)
            card.add_content(ticket)

    @pytest.mark.django_db
    def test_add_card_without_all_prerequisites_forced(self, card, profile, ticket, prerequisite):
        assert card.contents == []
        new_ticket = TicketFactory()
        ticket.must_have_all_prerequisites = True
        ticket.add_prerequisite(profile, "Require profile")
        ticket.add_prerequisite(new_ticket, "Require ticket")
        assert card.contents == []
        with freeze_time("2012-01-14"):
            card.add_content(profile)
            with pytest.raises(CardContentAddException) as excinfo:
                card.add_content(ticket)
            assert (
                str(excinfo.value) == f"Cannot add {ticket.name} because the card does not have required prerequisites."
            )

    @pytest.mark.django_db
    def test_add_card_without_all_prerequisites_forced_works(self, card, profile, ticket, prerequisite):
        assert card.contents == []
        new_ticket = TicketFactory()
        ticket.must_have_all_prerequisites = True
        ticket.add_prerequisite(profile, "Require profile")
        ticket.add_prerequisite(new_ticket, "Require ticket")
        assert card.contents == []
        with freeze_time("2012-01-14"):
            card.add_content(profile)
            card.add_content(new_ticket)
            card.add_content(ticket)
            assert card.contents == [profile, new_ticket, ticket]

    @pytest.mark.django_db
    def test_add_card_with_prerequisites(self, card, prerequisite):
        assert card.contents == []
        with freeze_time("2012-01-14"):
            card.add_content(prerequisite.secondary)
            card.add_content(prerequisite.primary)
            assert card.contents == [prerequisite.secondary, prerequisite.primary]

    @pytest.mark.django_db
    def test_get_content_expire_first(self, card):
        assert card.contents == []
        ticket_short = TicketFactory(validity=3600)
        ticket_long = TicketFactory(validity=7200)

        with freeze_time("2012-01-14"):
            card.add_content(ticket_short)
            card.add_content(ticket_long)
            assert ticket_short.validity == 3600
            assert ticket_long.validity == 7200
            assert card.contents == [ticket_short, ticket_long]
            assert card.get_content_to_use().content_object == ticket_short

    @pytest.mark.django_db
    def test_get_content_id_first(self, card):
        assert card.contents == []
        ticket_first = TicketFactory(validity=3600)
        ticket_second = TicketFactory(validity=3600)

        with freeze_time("2012-01-14"):
            card.add_content(ticket_first)
            card.add_content(ticket_second)
            assert card.contents == [ticket_first, ticket_second]
            assert card.get_content_to_use().content_object == ticket_first
