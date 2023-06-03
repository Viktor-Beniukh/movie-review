from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from subscribe.models import Subscriber

SUBSCRIBE_URL = reverse("subscribe:contact")
UNSUBSCRIBE_URL = reverse("subscribe:unsubscribe")


class PublicSubscribeTests(TestCase):

    def test_login_required_to_subscribe(self):
        response = self.client.get(SUBSCRIBE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateSubscribeTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        self.client.force_login(self.user)

        self.subscriber = Subscriber.objects.create(
            user=self.user,
            email=self.user.email
        )

    def test_create_subscribe(self):

        form_data = {
            "user": self.user,
            "email": self.user.email,
        }

        self.client.post(reverse("subscribe:contact"), data=form_data)
        new_subscribe = Subscriber.objects.get(user_id=form_data["user"])

        self.assertEqual(new_subscribe.user, form_data["user"])
        self.assertEqual(new_subscribe.email, form_data["email"])


class PublicUnsubscribeTests(TestCase):

    def test_login_required_to_unsubscribe(self):
        response = self.client.get(UNSUBSCRIBE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateUnsubscribeTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        self.client.force_login(self.user)

        self.subscriber = Subscriber.objects.create(
            user=self.user,
            email=self.user.email
        )

    def test_delete_unsubscribe(self):

        self.assertTrue(Subscriber.objects.filter(user=self.user).exists())

        self.user.subscriber.delete()

        self.assertFalse(Subscriber.objects.filter(user=self.user).exists())
