# Generated by Django 4.1.3 on 2022-11-26 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('uname', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('securityQuestion', models.CharField(max_length=255)),
            ],
        ),
    ]
