# Generated by Django 5.1.5 on 2025-01-23 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataLoadLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('success', models.BooleanField(blank=True, null=True)),
                ('message', models.TextField(blank=True, max_length=255, null=True)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(auto_now=True)),
                ('n_records', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_load_logs',
                'ordering': ['-started_at'],
            },
        ),
    ]