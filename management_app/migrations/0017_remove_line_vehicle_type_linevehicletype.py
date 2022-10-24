# Generated by Django 4.1.2 on 2022-10-17 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0016_alter_vehicle_plate_alter_vehicle_side_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='line',
            name='vehicle_type',
        ),
        migrations.CreateModel(
            name='LineVehicleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_app.line')),
                ('vehicle_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_app.vehicletype')),
            ],
        ),
    ]