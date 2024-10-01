# Generated by Django 5.1.1 on 2024-09-28 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haterade', '0002_loggedrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Strands',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('solution', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Sudoku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('boards', models.JSONField()),
            ],
        ),
        migrations.AddField(
            model_name='loggedrequest',
            name='agent',
            field=models.TextField(blank=True, null=True),
        ),
    ]