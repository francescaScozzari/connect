from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("scopus", "0002_scopusdocument"),
        ("xai", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TokensEmbeddings",
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
                ("data", models.JSONField(default=list)),
                (
                    "document",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tokens",
                        to="scopus.scopusdocument",
                        to_field="doi",
                    ),
                ),
            ],
            options={
                "verbose_name": "tokens embeddings",
                "verbose_name_plural": "tokens embeddings",
            },
        ),
    ]
