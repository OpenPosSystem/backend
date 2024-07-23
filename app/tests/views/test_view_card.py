import json
import pytest
from django.urls import reverse
from pos.models import Card, User
from ..factories import CardFactory


class TestViewCard:
    @pytest.mark.django_db
    def test_list_cards_as_user_empty(self, authenticated_user_client):
        url = reverse("pos_cards-list")
        response = authenticated_user_client.get(url, content_type="application/json")
        assert response.status_code == 200
        assert response.data == []

    @pytest.mark.django_db
    def test_list_cards_as_user(self, authenticated_user_client, card_user):
        url = reverse("pos_cards-list")
        response = authenticated_user_client.get(url, content_type="application/json")
        assert response.status_code == 200
        assert response.data == [{"uid": card_user.uid}]

    @pytest.mark.django_db
    def test_list_cards_as_user_multiple_cards(self, authenticated_user_client, user):
        url = reverse("pos_cards-list")
        cards = CardFactory.create_batch(5, user=user)
        response = authenticated_user_client.get(url, content_type="application/json")
        assert response.status_code == 200
        assert response.data == [{"uid": card.uid} for card in cards]

    @pytest.mark.django_db
    def test_list_cards_as_user_only_returns_his_cards(self, authenticated_user_client, card, card_user):
        url = reverse("pos_cards-list")
        response = authenticated_user_client.get(url, content_type="application/json")
        assert response.status_code == 200
        assert Card.objects.count() == 2
        assert response.data == [{"uid": card_user.uid}]

    @pytest.mark.django_db
    @pytest.mark.parametrize("num_cards", [1, 5, 20])
    def test_list_cards_as_admin_returns_all(self, num_cards, authenticated_admin_client, django_assert_num_queries):
        cards = CardFactory.create_batch(num_cards)
        url = reverse("pos_cards-list")
        with django_assert_num_queries(3):
            response = authenticated_admin_client.get(url, content_type="application/json")
            assert response.status_code == 200
            assert len(response.data) == num_cards
            assert Card.objects.count() == num_cards
            assert response.data == [{"uid": card.uid} for card in cards]

    @pytest.mark.django_db
    def test_user_can_read_his_card(self, authenticated_user_client, card_user, user):
        url = reverse("pos_cards-detail", kwargs={"uid": card_user.uid})
        response = authenticated_user_client.get(url, content_type="application/json")
        assert response.status_code == 200
        assert response.data == {
            "uid": card_user.uid,
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
            },
        }

    @pytest.mark.django_db
    def test_admin_can_read_any_card(self, authenticated_admin_client, card_user, user):
        url = reverse("pos_cards-detail", kwargs={"uid": card_user.uid})
        response = authenticated_admin_client.get(url, content_type="application/json")
        assert response.status_code == 200
        assert response.data == {
            "uid": card_user.uid,
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
            },
        }

    @pytest.mark.django_db
    def test_admin_can_update_card_full(self, authenticated_admin_client, card, user):
        url = reverse("pos_cards-detail", kwargs={"uid": card.uid})
        payload = {"uid": card.uid, "user_email": user.email}
        assert card.user != user
        response = authenticated_admin_client.put(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 200
        assert response.data == {
            "uid": card.uid,
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
            },
        }

    @pytest.mark.django_db
    def test_admin_can_update_card_full_ko(self, authenticated_admin_client, card, user):
        url = reverse("pos_cards-detail", kwargs={"uid": card.uid})
        payload = {"user_email": user.email}
        assert card.user != user
        response = authenticated_admin_client.put(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 400
        assert "uid" in response.data
        assert response.data["uid"][0].code == "required"
        assert str(response.data["uid"][0]) == "This field is required."

    @pytest.mark.django_db
    def test_admin_can_update_card_partial(self, authenticated_admin_client, card, user):
        url = reverse("pos_cards-detail", kwargs={"uid": card.uid})
        payload = {"user_email": user.email}
        assert card.user != user
        response = authenticated_admin_client.patch(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 200
        assert response.data == {
            "uid": card.uid,
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
            },
        }

    @pytest.mark.django_db
    def test_admin_update_inexistant_user(self, authenticated_admin_client, card):
        url = reverse("pos_cards-detail", kwargs={"uid": card.uid})
        payload = {"user_email": "doesnotexists@test.com"}
        assert User.objects.filter(email=payload["user_email"]).count() == 0
        response = authenticated_admin_client.patch(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 400
        assert "user_email" in response.data
        assert response.data["user_email"].code == "invalid"
        assert str(response.data["user_email"]) == "No user found with email doesnotexists@test.com"

    @pytest.mark.django_db
    def test_user_cannot_delete_his_card(self, authenticated_user_client, card_user, user):
        url = reverse("pos_cards-detail", kwargs={"uid": card_user.uid})
        response = authenticated_user_client.delete(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_admin_can_delete_any_card(self, authenticated_admin_client, card):
        url = reverse("pos_cards-detail", kwargs={"uid": card.uid})
        response = authenticated_admin_client.delete(url, content_type="application/json")
        assert response.status_code == 204
        with pytest.raises(Card.DoesNotExist) as excinfo:
            # This will throw an error as the card does not exists in the DB anymore
            card.refresh_from_db()
        assert str(excinfo.value) == "Card matching query does not exist."

    @pytest.mark.django_db
    def test_user_cannot_create_new_card(self, authenticated_user_client, user):
        url = reverse("pos_cards-list")
        response = authenticated_user_client.post(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_admin_can_create_new_card(self, authenticated_admin_client):
        url = reverse("pos_cards-list")
        payload = {"uid": "123456789"}
        response = authenticated_admin_client.post(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 201
        assert response.data == {"uid": payload["uid"], "user": None}
        card = Card.objects.get(uid=payload["uid"])
        assert card.uid == payload["uid"]
        assert card.user is None

    @pytest.mark.django_db
    def test_admin_can_create_new_card_with_user(self, authenticated_admin_client, user):
        url = reverse("pos_cards-list")
        payload = {
            "uid": "123456789",
            "user_email": user.email,
        }
        response = authenticated_admin_client.post(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 201
        assert response.data == {
            "uid": payload["uid"],
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
            },
        }
        card = Card.objects.get(uid=payload["uid"])
        assert card.uid == payload["uid"]
        assert card.user == user

    @pytest.mark.django_db
    def test_admin_can_create_new_card_with_user_unknown(self, authenticated_admin_client):
        url = reverse("pos_cards-list")
        payload = {
            "uid": "123456789",
            "user_email": "doesnotexists@test.com",
        }
        response = authenticated_admin_client.post(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 400
        assert "user_email" in response.data
        assert response.data["user_email"].code == "invalid"
        assert str(response.data["user_email"]) == "No user found with email doesnotexists@test.com"
