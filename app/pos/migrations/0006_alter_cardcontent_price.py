# Generated by Django 5.0.7 on 2024-07-19 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pos", "0005_cardcontent_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cardcontent",
            name="price",
            field=models.PositiveIntegerField(null=True),
        ),
    ]