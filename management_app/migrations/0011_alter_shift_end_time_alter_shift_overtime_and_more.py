# Generated by Django 4.1.2 on 2022-10-16 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0010_shiftonline_shifttime_remove_shift_shift_daytime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='shift',
            name='overtime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='shift',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]