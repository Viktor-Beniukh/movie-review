from django.contrib.auth import get_user_model
from django.test import TestCase

from subscribe.models import Subscriber


class SubscribeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(
            email="admin@user.com",
            password="admin12345",
        )
        Subscriber.objects.create(
            user=user,
            email=user.email
        )

    def test_subscribe_str(self):
        subscriber = Subscriber.objects.get(id=1)

        self.assertEqual(str(subscriber), subscriber.email)
