from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.test import TestCase
from django.urls import reverse

from movie.models import Movie, Category, Actor, Director, Genre


MOVIE_URL = reverse("movie:movie-list")


class PublicMovieTests(TestCase):

    def setUp(self):
        for i in range(1, 16):
            Movie.objects.create(title=f"Movie {i}", slug=f"movie-{i}")

    def test_pagination_with_unique_slug(self):
        paginator = Paginator(Movie.objects.all(), 10)

        self.assertEqual(paginator.count, 15)

        first_page = paginator.get_page(1)
        self.assertEqual(len(first_page.object_list), 10)
        self.assertTrue(first_page.has_next())

        second_page = paginator.get_page(2)
        self.assertEqual(len(second_page.object_list), 5)
        self.assertFalse(second_page.has_next())
        self.assertTrue(second_page.has_previous())


class PrivateCategoryTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        self.client.force_login(self.user)

    def test_create_category(self):
        form_data = {
            "name": "Films",
            "slug": "films",
        }

        self.client.post(reverse("movie:category-create"), data=form_data)
        new_category = Category.objects.get(name=form_data["name"])

        self.assertEqual(new_category.name, form_data["name"])
        self.assertEqual(new_category.slug, form_data["slug"])


class PrivateGenreTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        self.client.force_login(self.user)

    def test_create_genre(self):
        form_data = {
            "name": "Action",
            "slug": "action",
        }

        self.client.post(reverse("movie:genre-create"), data=form_data)
        new_genre = Genre.objects.get(name=form_data["name"])

        self.assertEqual(new_genre.name, form_data["name"])
        self.assertEqual(new_genre.slug, form_data["slug"])


class PrivateActorTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        self.client.force_login(self.user)

    def test_create_actor(self):
        form_data = {
            "name": "Tom Cruise",
            "age": 30
        }

        self.client.post(reverse("movie:actor-create"), data=form_data)
        new_actor = Actor.objects.get(name=form_data["name"])

        self.assertEqual(new_actor.name, form_data["name"])
        self.assertEqual(new_actor.age, form_data["age"])


class PrivateDirectorTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
        )
        self.client.force_login(self.user)

    def test_create_director(self):
        form_data = {
            "name": "Steven Spielberg",
            "age": 65
        }

        self.client.post(reverse("movie:director-create"), data=form_data)
        new_director = Director.objects.get(name=form_data["name"])

        self.assertEqual(new_director.name, form_data["name"])
        self.assertEqual(new_director.age, form_data["age"])
