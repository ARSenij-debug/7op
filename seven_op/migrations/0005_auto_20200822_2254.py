# Generated by Django 3.1 on 2020-08-22 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seven_op', '0004_auto_20200822_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='data',
            field=models.TextField(help_text='Текст блога'),
        ),
    ]
