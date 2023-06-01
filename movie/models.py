from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)
        index_together = (("id", "slug"),)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("movie:category-movies", kwargs={"slug": self.slug})


class Genre(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="directors/", null=True, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("movie:director-detail", kwargs={"slug": self.name})


class Actor(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="actors/", null=True, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("movie:actor-detail", kwargs={"slug": self.name})


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to="movies/", null=True, blank=True)
    year_of_release = models.PositiveSmallIntegerField(default=2023)
    country = models.CharField(max_length=255, blank=True)
    directors = models.ManyToManyField(Director, related_name="film_director")
    actors = models.ManyToManyField(Actor, related_name="film_actor")
    genres = models.ManyToManyField(Genre, related_name="film_genre")
    world_premiere = models.DateField(null=True, blank=True)
    budget = models.PositiveIntegerField(
        default=0, help_text="Enter amount in dollars"
    )
    fees_in_the_usa = models.PositiveIntegerField(
        default=0, help_text="Enter amount in dollars"
    )
    fees_in_the_world = models.PositiveIntegerField(
        default=0, help_text="Enter amount in dollars"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="film_category"
    )

    class Meta:
        ordering = ("title",)
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie:movie-detail", kwargs={"slug": self.slug})

    def get_review(self):
        return self.film_review.filter(parent__isnull=True)


class MovieFrames(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="movie_frames/", null=True, blank=True)
    movies = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="film_frames"
    )

    class Meta:
        ordering = ("title",)
        verbose_name = "Movie frame"
        verbose_name_plural = "Movie frames"

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_rating"
    )
    rating = models.IntegerField(default=1)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="film_rating"
    )

    def __str__(self):
        return f"{self.rating} - {self.movie}"


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_review"
    )
    text = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Parent"
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="film_review"
    )

    def __str__(self):
        return f"{self.user} - {self.movie}"
