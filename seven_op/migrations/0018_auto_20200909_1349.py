# Generated by Django 3.1 on 2020-09-09 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seven_op', '0017_auto_20200909_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogauthor',
            name='info',
            field=models.TextField(blank=True, help_text='необязательное поле', null=True, verbose_name='информация об авторе'),
        ),
    ]
