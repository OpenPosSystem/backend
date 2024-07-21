# Generated by Django 5.0.7 on 2024-07-19 22:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "business",
            "0004_alter_contract_price_alter_contract_turnstile_timer_and_more",
        ),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Incompatibility",
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
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created_at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated_at"),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Incompatibility"),
                ),
                ("primary_id", models.PositiveIntegerField()),
                ("secondary_id", models.PositiveIntegerField()),
                (
                    "primary_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="primary_incompatibilities",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "secondary_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="secondary_incompatibilities",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
