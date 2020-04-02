# Generated by Django 3.0.4 on 2020-04-02 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('version', models.BigIntegerField()),
                ('actor', models.CharField(blank=True, max_length=255, null=True)),
                ('class_name', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField()),
                ('event_name', models.CharField(max_length=255)),
                ('last_updated', models.DateTimeField()),
                ('new_value', models.TextField(blank=True, null=True)),
                ('old_value', models.TextField(blank=True, null=True)),
                ('persisted_object_id', models.CharField(blank=True, max_length=255, null=True)),
                ('persisted_object_version', models.CharField(blank=True, max_length=255, null=True)),
                ('property_name', models.CharField(blank=True, max_length=255, null=True)),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('uri', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'audit_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CmsUser',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('version', models.BigIntegerField()),
                ('active', models.BooleanField()),
                ('cname', models.CharField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField()),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('last_updated', models.DateTimeField()),
                ('medical_council_reg_no', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('password_hash', models.CharField(max_length=255)),
                ('tel', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('ehr_uid', models.CharField(blank=True, max_length=255, null=True)),
                ('priority', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('version', models.BigIntegerField()),
            ],
            options={
                'db_table': 'user_profile',
                'managed': False,
            },
        ),
    ]
