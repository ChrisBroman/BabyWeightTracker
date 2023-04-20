# Generated by Django 4.2 on 2023-04-20 02:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_alter_record_length"),
    ]

    operations = [
        migrations.AddField(
            model_name="baby",
            name="age_in_months",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(60),
                ],
            ),
        ),
    ]
