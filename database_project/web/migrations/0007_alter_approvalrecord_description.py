# Generated by Django 3.2.25 on 2024-12-07 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20241207_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalrecord',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
