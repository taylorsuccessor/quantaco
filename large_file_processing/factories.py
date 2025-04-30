import factory
from django.contrib.auth.models import User

from .models import Article


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = "test@gmail.com"
    password = factory.PostGenerationMethodCall("set_password", "testpassword")
