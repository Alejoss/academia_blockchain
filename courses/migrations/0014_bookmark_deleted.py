# Generated by Django 3.0.4 on 2020-11-19 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]