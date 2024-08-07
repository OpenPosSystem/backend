# Generated by Django 5.0.7 on 2024-07-19 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("business", "0002_profile_ticket"),
    ]

    operations = [
        migrations.AddField(
            model_name="contract",
            name="validity",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="profile",
            name="validity",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="ticket",
            name="entries",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="ticket",
            name="validity",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="contract",
            name="price",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="contract",
            name="turnstile_timer",
            field=models.IntegerField(default=3600),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="price",
            field=models.IntegerField(default=0),
        ),
    ]
