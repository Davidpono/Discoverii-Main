# Generated by Django 3.1.7 on 2021-03-31 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relecloud', '0002_auto_20210330_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cruise',
            name='destinations',
            field=models.ManyToManyField(related_name='cruises', to='relecloud.Destination'),
        ),
    ]