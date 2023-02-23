# Generated by Django 4.0.3 on 2022-04-29 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0009_alter_listing_purpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='i_have_currency',
            field=models.CharField(choices=[('CAD', 'CAD'), ('IRT', 'IRT'), ('MYR', 'MYR'), ('NZD', 'NZD'), ('USD', 'USD')], default='CAD', max_length=5),
        ),
        migrations.AddField(
            model_name='listing',
            name='i_want_currency',
            field=models.CharField(choices=[('CAD', 'CAD'), ('IRT', 'IRT'), ('MYR', 'MYR'), ('NZD', 'NZD'), ('USD', 'USD')], default='CAD', max_length=5),
        ),
        migrations.AlterField(
            model_name='listing',
            name='purpose',
            field=models.CharField(choices=[('GIFT', 'Gift'), ('HELP_MY_FAMILY', 'Help my family'), ('LOAN_REPAYMENT', 'Loan repayment'), ('TRAVELING', 'Traveling'), ('TUITION_FEE', 'Tuition fee')], default='TUITION_FEE', max_length=20),
        ),
    ]