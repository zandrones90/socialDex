# Generated by Django 3.1.3 on 2020-11-29 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20201129_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diocane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usern', models.CharField(max_length=100)),
                ('nofposts', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Postadmin',
        ),
    ]