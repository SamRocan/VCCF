# Generated by Django 3.2.16 on 2022-11-05 08:51

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('api', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('variables', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Founder',
            fields=[
                ('ph_username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('company', models.ManyToManyField(to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='TwitterInfo',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('scores', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), size=None)),
                ('founder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.founder')),
            ],
        ),
    ]