# Generated by Django 3.0.7 on 2020-07-02 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADVANCE', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uploadfile',
            options={'permissions': [('access_Advance', 'Can access 高级功能')], 'verbose_name': '上传文件信息表'},
        ),
    ]
