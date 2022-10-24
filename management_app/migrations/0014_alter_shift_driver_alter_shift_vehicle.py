# Generated by Django 4.1.2 on 2022-10-16 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0013_alter_shift_end_time_alter_shift_overtime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management_app.driver'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management_app.vehicle'),
        ),
    ]