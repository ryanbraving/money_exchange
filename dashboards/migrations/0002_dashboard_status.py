# Generated by Django 4.0.3 on 2023-03-15 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='status',
            field=models.IntegerField(choices=[(0, 'Enabled'), (1, 'Suspended'), (2, 'Disabled')], db_index=True, default=0),
        ),
    ]
