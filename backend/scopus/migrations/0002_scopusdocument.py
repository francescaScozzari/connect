from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scopus", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScopusDocument",
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
                ("data", models.JSONField()),
            ],
        ),
    ]
