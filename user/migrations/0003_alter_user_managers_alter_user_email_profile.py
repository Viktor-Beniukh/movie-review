# Generated by Django 4.2.1 on 2023-05-31 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_add_user"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", user.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
        migrations.CreateModel(
            name="Profile",
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
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="user_profile/"),
                ),
                ("bio", models.TextField(blank=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]