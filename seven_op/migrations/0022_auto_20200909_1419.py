# Generated by Django 3.1 on 2020-09-09 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seven_op', '0021_auto_20200909_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(blank=True, help_text='необязательное поле', max_length=1000, null=True, verbose_name='описание'),
        ),
    ]
