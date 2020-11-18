# Generated by Django 3.1.3 on 2020-11-14 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drugdb', '0018_remove_registereddrug_cmsinv_item'),
        ('inventory', '0041_auto_20201114_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='reg_drug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='drugdb.registereddrug'),
        ),
    ]