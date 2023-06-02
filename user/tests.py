from django.test import TestCase


from user.models import User


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email="admin@user.com",
            password="admin12345",
        )

    def test_user_str(self):
        user = User.objects.get(id=1)

        self.assertEqual(str(user), f"{user}")
