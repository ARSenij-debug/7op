# Generated by Django 3.1 on 2020-09-28 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seven_op', '0025_auto_20200928_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paragraph',
            name='paragraph_img',
            field=models.ImageField(blank=True, upload_to='seven_op/static/uploads/files/%Y/%m/%d', verbose_name='фото к параграфу'),
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='paragraph_nb',
            field=models.IntegerField(blank=True, default=0, verbose_name='номер параграфа'),
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='paragraph_text',
            field=models.TextField(blank=True, verbose_name='текст параграфа'),
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='paragraph_title',
            field=models.CharField(blank=True, max_length=200, verbose_name='заголовок параграфа'),
        ),
    ]
