# Generated by Django 3.0.4 on 2021-07-25 23:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0009_auto_20210724_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificaterequest',
            name='state',
            field=models.CharField(blank=True, choices=[('ACCEPTED', 'accepted'), ('REJECTED', 'rejected'), ('DELETED', 'deleted'), ('PENDING', 'pending')], default='PENDING', max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='certificaterequest',
            unique_together={('user', 'event')},
        ),
    ]
