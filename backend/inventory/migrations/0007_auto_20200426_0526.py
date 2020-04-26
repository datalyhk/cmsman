# Generated by Django 3.0.4 on 2020-04-25 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20200425_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.Category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='inventory_type',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='inventory.ItemType'),
        ),
    ]