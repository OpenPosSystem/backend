from rest_framework import serializers
from .user import UserSerializer
from ..models import Card, User
from rest_framework.exceptions import ValidationError


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["uid"]


class CardDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Card
        fields = ["uid", "user", "user_email"]

    def create(self, validated_data):
        user_email = validated_data.pop("user_email", None)
        card = Card(**validated_data)

        if user_email:
            try:
                user = User.objects.get(email=user_email)
                card.user = user
            except User.DoesNotExist:
                raise ValidationError({"user_email": f"No user found with email {user_email}"})

        card.save()
        return card

    def update(self, instance, validated_data):
        user_email = validated_data.pop("user_email", None)
        if user_email:
            try:
                user = User.objects.get(email=user_email)
                instance.user = user
            except User.DoesNotExist:
                raise ValidationError({"user_email": f"No user found with email {user_email}"})

        instance.uid = validated_data.get("uid", instance.uid)
        instance.save()
        return instance
