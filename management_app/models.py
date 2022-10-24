from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.functions import Cast


# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    date_of_birth = models.DateField()
    position = models.CharField(max_length=30)
    CONTRACT = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('FR', 'Freelancer'),
    ]
    contract = models.CharField(max_length=2, choices=CONTRACT)
    contract_start = models.DateField()
    contract_end = models.DateField(default="9999-12-31")

    def __str__(self):
        return f'ID: {self.pk} | {self.user.first_name} {self.user.last_name}'


class VehicleType(models.Model):
    VEHICLE_TYPE = [
        ('MINIBUS', 'Minibus'),
        ('BUS', 'Standard bus'),
        ('ARTICULATED BUS', 'Articulated Bus'),
        ('SHORT TRAM', 'Short Tram'),
        ('LONG TRAM', 'Long Tram'),
    ]
    name = models.CharField(max_length=30, choices=VEHICLE_TYPE)
    ENGINE = [
        ('E', 'Electric'),
        ('D', 'Diesel'),
        ('H', 'Hybrid'),
    ]
    engine = models.CharField(max_length=1, choices=ENGINE)

    def __str__(self):
        return f'{self.name} {self.engine}'


class VehicleModel(models.Model):
    name = models.CharField(max_length=60)
    type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class Vehicle(models.Model):
    side_number = models.CharField(max_length=10, unique=True)
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    plate = models.CharField(max_length=10, unique=True)
    production_date = models.DateField()
    last_review = models.DateField()
    next_review = models.DateField()

    def __str__(self):
        return f'{self.side_number}'

    class Meta:
        ordering = [
            Cast("side_number", output_field=models.IntegerField()),
        ]


class Driver(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    license_validity = models.DateField()
    vehicle_assigned = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.pk}'


class Line(models.Model):
    name = models.CharField(max_length=30, unique=True)
    distance = models.IntegerField()
    vehicle_type = models.ManyToManyField(VehicleType, through="LineVehicleType", blank=True)
    first_stop = models.CharField(max_length=50)
    last_stop = models.CharField(max_length=50)

    class Meta:
        ordering = [
            Cast("name", output_field=models.IntegerField()),
        ]

    def __str__(self):
        return f'{self.name}'


class LineVehicleType(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)


class ShiftTime(models.Model):
    line = models.ManyToManyField(Line, through='ShiftOnLine')
    DAY = [
        ('WD', 'Weekday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    day = models.CharField(max_length=3, choices=DAY)
    DAYTIME = [
        ('M', 'Morning'),
        ('A', 'Afternoon'),
        ('N', 'Night'),
    ]
    daytime = models.CharField(max_length=1, choices=DAYTIME)
    order = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.day} {self.daytime}'


class ShiftOnLine(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    shift_time = models.ForeignKey(ShiftTime, on_delete=models.CASCADE)
    number_of_shifts = models.IntegerField(null=True)

    def __str__(self):
        return f'Line: {self.line}|Shift-time: {self.shift_time}|Number of shifts: {self.number_of_shifts}'


class Shift(models.Model):
    date = models.DateField()
    shift_on_line = models.ForeignKey(ShiftOnLine, on_delete=models.CASCADE, null=True)
    shift_number = models.IntegerField(null=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    overtime = models.TimeField(null=True, blank=True)

    def duration(self):
        return self.end_time - self.start_time + self.overtime

    def __str__(self):
        return f'Line: {self.shift_on_line.line.name} - {self.shift_on_line.shift_time.day}' \
               f'{self.shift_on_line.shift_time.daytime} - No. on the line: {self.shift_number}'

# class Breakdown(models.Model):
#     bus = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     breakdown_date = models.DateField()
#     repair_date = models.DateField()
#     mechanic = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     description = models.TextField()
