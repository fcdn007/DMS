# Generated by Django 3.0.7 on 2020-08-12 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMR', '0002_auto_20200812_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followupinfo',
            name='survival_status',
            field=models.CharField(blank=True, db_column='生存状态', default='存活', max_length=10, null=True),
        ),
    ]