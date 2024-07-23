import pytest
from django.urls import reverse


class TestViewContract:
    @pytest.mark.django_db
    def test_user_cannot_list_business_contracts(self, authenticated_user_client):
        url = reverse("business_contracts-list")
        response = authenticated_user_client.get(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_create_business_contracts(self, authenticated_user_client):
        url = reverse("business_contracts-list")
        response = authenticated_user_client.post(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_update_partial_business_contracts(self, authenticated_user_client, contract):
        url = reverse("business_contracts-detail", kwargs={"pk": contract.id})
        response = authenticated_user_client.patch(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_update_business_contracts(self, authenticated_user_client, contract):
        url = reverse("business_contracts-detail", kwargs={"pk": contract.id})
        response = authenticated_user_client.put(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_delete_business_contracts(self, authenticated_user_client, contract):
        url = reverse("business_contracts-detail", kwargs={"pk": contract.id})
        response = authenticated_user_client.delete(url, content_type="application/json")
        assert response.status_code == 403
