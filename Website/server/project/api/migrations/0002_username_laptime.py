# Generated by Django 5.2.1 on 2025-06-04 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='username',
            name='laptime',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
