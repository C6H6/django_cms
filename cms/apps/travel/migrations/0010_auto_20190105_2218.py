# Generated by Django 2.1.2 on 2019-01-05 21:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0009_auto_20190105_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 19, 21, 18, 27, 967876, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='travel',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 12, 21, 18, 27, 967840, tzinfo=utc)),
        ),
    ]