# Generated by Django 4.0.3 on 2022-05-08 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0013_alter_listing_buying_alter_listing_buying_currency_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='is_complete',
            new_name='is_completed',
        ),
    ]
