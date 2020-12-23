# Generated by Django 3.1.4 on 2020-12-22 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Influencer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('platform', models.CharField(choices=[('Instagram', 'Instagram')], max_length=50)),
                ('picture', models.URLField()),
            ],
        ),
    ]