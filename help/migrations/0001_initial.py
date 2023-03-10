# Generated by Django 4.1.6 on 2023-02-10 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.IntegerField(choices=[(1, 'Contact'), (2, 'Reporting a Problem'), (3, 'Help Request')], default=1)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.TextField(max_length=128)),
                ('content', models.TextField(max_length=2048)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
