# Generated by Django 2.1 on 2019-07-09 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0003_auto_20190706_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='max',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=8),
        ),
    ]