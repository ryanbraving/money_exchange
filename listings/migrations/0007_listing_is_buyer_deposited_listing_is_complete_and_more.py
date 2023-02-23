# Generated by Django 4.0.3 on 2022-04-24 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_alter_listing_i_have_alter_listing_i_want'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_buyer_deposited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='is_seller_deposited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='listing',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]