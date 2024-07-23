import pytest
from django.urls import reverse


class TestViewProfile:
    @pytest.mark.django_db
    def test_user_cannot_list_profiles(self, authenticated_user_client):
        url = reverse("business_profiles-list")
        response = authenticated_user_client.get(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_create_profiles(self, authenticated_user_client):
        url = reverse("business_profiles-list")
        response = authenticated_user_client.post(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_update_partial_profiles(self, authenticated_user_client, profile):
        url = reverse("business_profiles-detail", kwargs={"pk": profile.id})
        response = authenticated_user_client.patch(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_update_profiles(self, authenticated_user_client, profile):
        url = reverse("business_profiles-detail", kwargs={"pk": profile.id})
        response = authenticated_user_client.put(url, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user_cannot_delete_profiles(self, authenticated_user_client, profile):
        url = reverse("business_profiles-detail", kwargs={"pk": profile.id})
        response = authenticated_user_client.delete(url, content_type="application/json")
        assert response.status_code == 403
