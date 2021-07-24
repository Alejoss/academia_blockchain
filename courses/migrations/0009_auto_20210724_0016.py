# Generated by Django 3.0.4 on 2021-07-24 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20210714_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificaterequest',
            name='accepted',
        ),
        migrations.RemoveField(
            model_name='certificaterequest',
            name='deleted',
        ),
        migrations.AddField(
            model_name='certificaterequest',
            name='state',
            field=models.CharField(blank=True, choices=[('ACCEPTED', 'accepted'), ('DENIED', 'denied'), ('DELETED', 'deleted'), ('PENDING', 'pending')], max_length=50),
        ),
    ]
