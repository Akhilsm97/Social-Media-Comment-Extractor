# Generated by Django 3.0.4 on 2021-08-23 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_addfriendnew'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
            ],
        ),
    ]