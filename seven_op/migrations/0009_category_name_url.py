# Generated by Django 3.1 on 2020-08-23 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seven_op', '0008_auto_20200823_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_url',
            field=models.CharField(default=1, help_text='название, которое будет отображаться в ссылках', max_length=200),
            preserve_default=False,
        ),
    ]
