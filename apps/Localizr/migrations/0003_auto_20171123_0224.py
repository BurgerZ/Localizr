# Generated by Django 2.0b1 on 2017-11-23 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Localizr', '0002_auto_20171123_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appinfo',
            name='base_locale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Localizr.Locale'),
        ),
    ]
