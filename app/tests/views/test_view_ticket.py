import pytest
from django.urls import reverse


class TestViewTicket:
    @pytest.mark.django_db
    def test_user_cannot_list_business_tickets(self, authenticated_user_client):
        url = reverse("business_tickets-list")
        response = authenticated_user_client.get(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_create_business_tickets(self, authenticated_user_client):
        url = reverse("business_tickets-list")
        response = authenticated_user_client.post(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_update_partial_business_tickets(self, authenticated_user_client, ticket):
        url = reverse("business_tickets-detail", kwargs={"pk": ticket.id})
        response = authenticated_user_client.patch(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_update_business_tickets(self, authenticated_user_client, ticket):
        url = reverse("business_tickets-detail", kwargs={"pk": ticket.id})
        response = authenticated_user_client.put(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_delete_business_tickets(self, authenticated_user_client, ticket):
        url = reverse("business_tickets-detail", kwargs={"pk": ticket.id})
        response = authenticated_user_client.delete(url, content_type="application/json")
        assert response.status_code == 403
