# Generated by Django 3.0.7 on 2020-08-13 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMR', '0004_auto_20200812_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='liverpathologicalinfo',
            name='raw_id',
            field=models.CharField(blank=True, db_column='病理编号', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='liverpathologicalinfo',
            name='tumor1_diam',
            field=models.FloatField(blank=True, db_column='肿瘤最大径', null=True),
        ),
    ]
