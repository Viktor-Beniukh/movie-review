from django.test import TestCase

from movie.models import (
    Category,
    Actor,
    Director,
    Genre,
    Movie,
    MovieFrames,
)


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="Films", slug="films")

    def test_category_str(self):
        category = Category.objects.get(id=1)

        self.assertEqual(str(category), f"{category.name}")

    def test_get_absolute_url(self):
        category = Category.objects.get(slug="films")

        self.assertEqual(category.get_absolute_url(), "/category/films/")


class ActorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Actor.objects.create(name="Tom Cruise")

    def test_actor_str(self):
        actor = Actor.objects.get(id=1)

        self.assertEqual(str(actor), f"{actor.name}")

    def test_get_absolute_url(self):
        actor = Actor.objects.get(name="Tom Cruise")

        self.assertEqual(actor.get_absolute_url(), "/actor/Tom%20Cruise/")


class DirectorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Director.objects.create(name="Steven Spielberg")

    def test_director_str(self):
        director = Director.objects.get(id=1)

        self.assertEqual(str(director), f"{director.name}")

    def test_get_absolute_url(self):
        director = Director.objects.get(name="Steven Spielberg")

        self.assertEqual(director.get_absolute_url(), "/director/Steven%20Spielberg/")


class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name="Action", slug="action")

    def test_genre_str(self):
        genre = Genre.objects.get(id=1)

        self.assertEqual(str(genre), f"{genre.name}")


class MovieModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Movie.objects.create(
            title="Minority Report",
            slug="minority-report",
        )

    def test_get_absolute_url(self):
        movie = Movie.objects.get(slug="minority-report")

        self.assertEqual(movie.get_absolute_url(), "/minority-report/")


class MovieFramesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        movie = Movie.objects.create(
            title="Minority Report",
            slug="minority-report",
        )

        MovieFrames.objects.create(
            title="Frame to Minority Report",
            movies=movie
        )

    def test_movie_frame_str(self):
        frame = MovieFrames.objects.get(id=1)

        self.assertEqual(str(frame), f"{frame.title}")
