import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: list = []

    operations = [
        migrations.CreateModel(
            name="Author",
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
                ("orcid", models.CharField(max_length=19, unique=True)),
                ("full_name", models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name="University",
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
                ("name", models.CharField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Document",
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
                ("doi", models.CharField(unique=True)),
                ("title", models.CharField()),
                ("description", models.TextField()),
                (
                    "authors",
                    models.ManyToManyField(
                        related_name="documents", to="universities.author"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="author",
            name="university",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="authors",
                to="universities.university",
            ),
        ),
    ]
