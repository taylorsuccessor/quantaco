from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Article


# Optionally, you can create a User serializer if you need detailed user information
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class ArticleSerializer(serializers.ModelSerializer):
    # Adding extra fields
    formatted_created_at = serializers.SerializerMethodField()
    author_details = UserSerializer(source="author", read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "content",
            "author",
            "author_details",
            "created_at",
            "formatted_created_at",
        )

    def get_formatted_created_at(self, obj):
        # Example of adding a custom method field
        return obj.created_at.strftime("%B %d, %Y %H:%M:%S")

    def validate_title(self, value):
        # Example of custom validation
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title is too short. It should be at least 5 characters."
            )
        return value

    def validate(self, data):
        # Example of custom validation logic
        if data["content"].startswith("Forbidden"):
            raise serializers.ValidationError({"content": "Content cannot start with 'Forbidden'."})
        return data

    def create(self, validated_data):
        # Example of custom create logic
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Example of custom update logic
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
