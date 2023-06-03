# Generated by Django 4.2.1 on 2023-05-30 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Actor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("age", models.PositiveSmallIntegerField(default=0)),
                ("description", models.TextField(blank=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="actors/"),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "ordering": ("name",),
                "index_together": {("id", "slug")},
            },
        ),
        migrations.CreateModel(
            name="Director",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("age", models.PositiveSmallIntegerField(default=0)),
                ("description", models.TextField(blank=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="directors/"),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "ordering": ("name",),
                "index_together": {("id", "slug")},
            },
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(db_index=True, max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("tagline", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "poster",
                    models.ImageField(blank=True, null=True, upload_to="movies/"),
                ),
                ("year_of_release", models.PositiveSmallIntegerField(default=2023)),
                ("country", models.CharField(blank=True, max_length=255)),
                ("world_premiere", models.DateField(blank=True, null=True)),
                (
                    "budget",
                    models.PositiveIntegerField(
                        default=0, help_text="Enter amount in dollars"
                    ),
                ),
                (
                    "fees_in_the_usa",
                    models.PositiveIntegerField(
                        default=0, help_text="Enter amount in dollars"
                    ),
                ),
                (
                    "fees_in_the_world",
                    models.PositiveIntegerField(
                        default=0, help_text="Enter amount in dollars"
                    ),
                ),
                (
                    "actors",
                    models.ManyToManyField(related_name="film_actor", to="movie.actor"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="film_category",
                        to="movie.category",
                    ),
                ),
                (
                    "directors",
                    models.ManyToManyField(
                        related_name="film_director", to="movie.director"
                    ),
                ),
                (
                    "genres",
                    models.ManyToManyField(related_name="film_genre", to="movie.genre"),
                ),
            ],
            options={
                "ordering": ("title",),
                "index_together": {("id", "slug")},
            },
        ),
        migrations.CreateModel(
            name="RatingStar",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.IntegerField()),
            ],
            options={
                "ordering": ("-value",),
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(blank=True)),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="film_review",
                        to="movie.movie",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="movie.review",
                        verbose_name="Parent",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_review",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="film_rating",
                        to="movie.movie",
                    ),
                ),
                (
                    "star",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="star_rating",
                        to="movie.ratingstar",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_rating",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MovieFrames",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="movie_frames/"),
                ),
                (
                    "movies",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="film_frames",
                        to="movie.movie",
                    ),
                ),
            ],
            options={
                "verbose_name": "Movie frame",
                "verbose_name_plural": "Movie frames",
                "ordering": ("title",),
            },
        ),
    ]
