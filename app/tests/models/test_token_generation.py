from datetime import datetime, timedelta

import pytest
import json
from django.urls import reverse
import jwt
from django.conf import settings
from freezegun import freeze_time
from rest_framework_simplejwt.tokens import RefreshToken


class TestTokenGeneration:
    @pytest.mark.django_db
    def test_get_token(self, api_client, user):
        url = reverse("token_obtain_pair")
        data = {"email": user.email, "password": "password"}
        with freeze_time("2012-01-14") as current_time:
            response = api_client.post(url, data=json.dumps(data), content_type="application/json")
            assert response.status_code == 200

            # We perform checks on the access token
            jwt_data_access = response.data["access"]
            jwt_decoded_data_access = jwt.decode(jwt_data_access, settings.SECRET_KEY, algorithms=["HS256"])
            assert jwt_decoded_data_access["token_type"] == "access"
            assert jwt_decoded_data_access["user_id"] == user.id
            assert datetime.fromtimestamp(jwt_decoded_data_access["iat"]) == current_time.time_to_freeze
            assert datetime.fromtimestamp(jwt_decoded_data_access["exp"]) == current_time.time_to_freeze + timedelta(
                minutes=5
            )

            # We perform checks on the access refresh
            jwt_data_refresh = response.data["refresh"]
            jwt_decoded_data_refresh = jwt.decode(jwt_data_refresh, settings.SECRET_KEY, algorithms=["HS256"])
            assert jwt_decoded_data_refresh["token_type"] == "refresh"
            assert jwt_decoded_data_refresh["user_id"] == user.id
            assert datetime.fromtimestamp(jwt_decoded_data_refresh["iat"]) == current_time.time_to_freeze
            assert datetime.fromtimestamp(jwt_decoded_data_refresh["exp"]) == current_time.time_to_freeze + timedelta(
                days=1
            )

    @pytest.mark.django_db
    def test_get_token_wrong_password(self, api_client, user):
        url = reverse("token_obtain_pair")
        response = api_client.post(
            url,
            data=json.dumps({"email": user.email, "password": "test"}),
            content_type="application/json",
        )
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_get_token_missing_data(self, api_client, user):
        url = reverse("token_obtain_pair")
        response = api_client.post(
            url,
            data=json.dumps(
                {
                    "email": user.email,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_refresh_token(self, api_client, user):
        with freeze_time("2012-01-14") as current_time:
            tokens = RefreshToken.for_user(user)
            url = reverse("token_refresh")
            data = {
                "refresh": str(tokens),
            }
            response = api_client.post(url, data=json.dumps(data), content_type="application/json")
            assert response.status_code == 200
            # We perform checks on the access token
            jwt_data_access = response.data["access"]
            jwt_decoded_data_access = jwt.decode(jwt_data_access, settings.SECRET_KEY, algorithms=["HS256"])
            assert jwt_decoded_data_access["token_type"] == "access"
            assert jwt_decoded_data_access["user_id"] == user.id
            assert datetime.fromtimestamp(jwt_decoded_data_access["iat"]) == current_time.time_to_freeze
            assert datetime.fromtimestamp(jwt_decoded_data_access["exp"]) == current_time.time_to_freeze + timedelta(
                minutes=5
            )
