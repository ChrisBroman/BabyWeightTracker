# Generated by Django 4.2 on 2023-04-19 20:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="baby",
            options={"verbose_name_plural": "Babies"},
        ),
        migrations.AddField(
            model_name="baby",
            name="current_weight",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(2500),
                    django.core.validators.MaxValueValidator(5000),
                ],
            ),
        ),
    ]
