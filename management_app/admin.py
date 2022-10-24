from django.contrib import admin

from management_app.models import Employee, Line, VehicleType, Shift, ShiftTime, ShiftOnLine

# Register your models here.
admin.site.register(Employee)
admin.site.register(Line)
admin.site.register(VehicleType)
admin.site.register(Shift)
admin.site.register(ShiftTime)
admin.site.register(ShiftOnLine)
