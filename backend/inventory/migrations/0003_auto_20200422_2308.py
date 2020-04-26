# Generated by Django 3.0.4 on 2020-04-22 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20200422_2152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='delivery',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Deliveries'},
        ),
        migrations.AlterModelOptions(
            name='itemdelivery',
            options={'ordering': ['received_date'], 'verbose_name_plural': 'ItemDeliveries'},
        ),
        migrations.RemoveField(
            model_name='item',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='item',
            name='unit_price',
        ),
    ]
