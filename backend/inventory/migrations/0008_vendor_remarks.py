# Generated by Django 3.0.4 on 2020-04-25 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20200426_0526'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]
