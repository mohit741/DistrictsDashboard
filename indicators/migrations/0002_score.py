# Generated by Django 2.1 on 2019-07-06 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0002_auto_20190705_1511'),
        ('indicators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('composite', models.DecimalField(decimal_places=3, max_digits=7)),
                ('rank', models.PositiveIntegerField()),
                ('period', models.DateField()),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='block_score', to='regions.Block')),
            ],
        ),
    ]