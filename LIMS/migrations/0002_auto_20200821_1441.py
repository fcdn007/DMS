# Generated by Django 3.0.7 on 2020-08-21 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LIMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='methypoolinginfo',
            name='singleLB_Pooling_id',
            field=models.CharField(blank=True, db_column='测序文库编号', max_length=80, null=True, unique=True),
        ),
    ]
