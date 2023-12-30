# Generated by Django 4.2.7 on 2023-12-23 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wisewallet', '0004_delete_expense'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('label', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
