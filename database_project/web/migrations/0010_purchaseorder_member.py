# Generated by Django 3.2.25 on 2024-12-07 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_alter_category_threshold'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='member',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='web.member'),
            preserve_default=False,
        ),
    ]
