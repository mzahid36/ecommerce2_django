# Generated by Django 4.2 on 2023-08-30 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_getintouch'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=150)),
                ('persons', models.CharField(choices=[('Number of guests 1', '1'), ('Number of guests 2', '2'), ('Number of guests 3', '3'), ('Number of guests 4', '4'), ('Number of guests 5', '5')], max_length=50)),
                ('phone', models.CharField(max_length=14)),
                ('note', models.TextField()),
                ('date', models.DateField()),
                ('datetime', models.DateTimeField()),
                ('time', models.TimeField()),
                ('duration', models.DurationField()),
            ],
        ),
    ]
