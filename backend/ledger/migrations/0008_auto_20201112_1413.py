# Generated by Django 3.1.3 on 2020-11-12 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0007_expensecategory_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expensecategory',
            options={'ordering': ['code', '-active'], 'verbose_name': 'Expense category', 'verbose_name_plural': 'Expense categories'},
        ),
        migrations.RemoveField(
            model_name='expensecategory',
            name='label',
        ),
        migrations.AlterField(
            model_name='expensecategory',
            name='code',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]