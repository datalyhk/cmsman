# Generated by Django 3.1.3 on 2021-02-11 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0057_auto_20210128_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='is_supplier',
            field=models.BooleanField(default=True),
        ),
    ]