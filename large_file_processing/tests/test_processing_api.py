from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ProcessingAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

    def test_article_list(self):
        url = reverse("ijson-start-processing-ijson-celery")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.json() == {"status": "processing started"}
