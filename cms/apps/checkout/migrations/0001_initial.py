# Generated by Django 2.1.2 on 2019-01-05 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('travel', '0009_auto_20190105_2214'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_first_name', models.CharField(max_length=100)),
                ('customer_last_name', models.CharField(max_length=100)),
                ('customer_address', models.CharField(max_length=100)),
                ('customer_city', models.CharField(max_length=50)),
                ('customer_phone', models.CharField(max_length=15)),
                ('passengers', models.IntegerField()),
                ('passengers_data', models.TextField()),
                ('travel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.Travel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]