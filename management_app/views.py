from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from management_app.forms import LoginForm, EditShiftForm, VehicleForm, DriverForm, LineForm
from management_app.models import Line, ShiftOnLine, Shift, Vehicle, VehicleType, Driver, ShiftTime


# Create your views here.
class IndexView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth_form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'auth_form.html', {'form': form, 'message': 'Wrong username or password'})
            else:
                login(request, user)
                url = request.GET.get('next', 'index')
                return redirect(url)
        return render(request, 'auth_form.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class LinesView(View):
    def get(self, request):
        lines = Line.objects.all()
        return render(request, 'lines.html', {'lines': lines})


class AddLineView(LoginRequiredMixin, View):
    def get(self, request):
        header = "Add Line"
        form = LineForm()
        return render(request, 'form.html', {'form': form, 'header': header})

    def post(self, request):
        header = "Add Line"
        form = LineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lines')
        else:
            return render(request, 'form.html', {'form': form, 'header': header})


class EditLineView(LoginRequiredMixin, View):
    def get(self, request, line_id):
        line = Line.objects.get(pk=line_id)
        form = LineForm(instance=line)

        header = f"Edit Line {line.name}"
        return render(request, 'form.html', {'form': form, 'header': header})

    def post(self, request, line_id):
        line = Line.objects.get(pk=line_id)
        form = LineForm(request.POST, instance=line)
        if form.is_valid():
            form.save()
            return redirect('lines')
        else:
            header = f"Edit Line {line.name}"
            return render(request, 'form.html', {'form': form, 'header': header})


class DeleteLineView(LoginRequiredMixin, View):
    def get(self, request, line_id):
        line = Line.objects.get(pk=line_id)
        line.delete()
        return redirect('lines')


class LineShiftDetailView(View):
    def get(self, request, line_id):
        shift_on_line = ShiftOnLine.objects.filter(line_id=line_id).order_by('shift_time__order')
        line = Line.objects.get(pk=line_id)
        return render(request, 'line_shift_details.html', {'shift_on_line': shift_on_line,
                                                           'line': line})


class AddLineShiftView(LoginRequiredMixin, View):
    def get(self, request, line_id):
        line = Line.objects.get(pk=line_id)
        shift_time = ShiftTime.objects.all()
        return render(request, 'add_line_shift.html', {'line': line,
                                                       'shift_time': shift_time})

    def post(self, request, line_id):
        line = Line.objects.get(pk=line_id)
        shift_time_id = request.POST['shift_time']
        shift_time = ShiftTime.objects.get(pk=shift_time_id)
        number_of_shifts = request.POST['number_of_shifts']
        ShiftOnLine(line=line, shift_time=shift_time, number_of_shifts=number_of_shifts).save()
        return redirect(f'/line/shifts/{line_id}')


class EditLineShiftView(LoginRequiredMixin, View):
    def get(self, request, line_id, shift_id):
        line = Line.objects.get(pk=line_id)
        shift_on_line = ShiftOnLine.objects.get(pk=shift_id)
        shift_time = ShiftTime.objects.all()
        return render(request, 'edit_line_shift.html', {'line': line,
                                                        'shift_on_line': shift_on_line,
                                                        'shift_time': shift_time})

    def post(self, request, line_id, shift_id):
        line = Line.objects.get(pk=line_id)
        shift_time_id = request.POST['shift_time']
        shift_time = ShiftTime.objects.get(pk=shift_time_id)
        number_of_shifts = request.POST['number_of_shifts']

        shift_on_line = ShiftOnLine.objects.get(pk=shift_id)
        shift_on_line.line = line
        shift_on_line.shift_time = shift_time
        shift_on_line.number_of_shifts = number_of_shifts
        shift_on_line.save()
        return redirect(f'/line/shifts/{line_id}')


class DeleteLineShiftView(LoginRequiredMixin, View):
    def get(self, request, line_id, shift_id):
        shift_on_line = ShiftOnLine.objects.get(pk=shift_id)
        shift_on_line.delete()
        return redirect(f'/line/shifts/{line_id}')


class ShiftsOnLinesView(View):
    def get(self, request):
        lines = Line.objects.all()
        shift_line = ShiftOnLine.objects.all().order_by('shift_time__order')
        current_date = date.today()
        return render(request, 'shifts.html', {'lines': lines,
                                               'shift_line': shift_line,
                                               'current_date': current_date})


class ShiftsOnLineDetailView(View):
    def get(self, request, line_id, shift_date):
        line = Line.objects.get(pk=line_id)
        shifts = Shift.objects.filter(shift_on_line__line_id=line_id, date=shift_date)
        if shift_date.weekday() <= 4:
            shift_day = "WD"
        elif shift_date.weekday() == 5:
            shift_day = "SAT"
        elif shift_date.weekday() == 6:
            shift_day = "SUN"
        shifts_on_line = ShiftOnLine.objects.filter(line_id=line_id, shift_time__day=shift_day)

        all_lines = Line.objects.all()
        current_date = date.today()
        return render(request, 'line_shifts_details.html', {'line': line,
                                                            'shifts': shifts,
                                                            'shift_date': shift_date,
                                                            'shifts_on_line': shifts_on_line,
                                                            'all_lines': all_lines,
                                                            'current_date': current_date})

    def post(self, request, line_id, shift_date):
        line_id = request.POST['line_id']
        shift_date = request.POST['shift_date']
        return redirect(f'/shifts/{line_id}/{shift_date}')


class AddShiftLineDateView(LoginRequiredMixin, View):
    def get(self, request, line_id, shift_date):
        line = Line.objects.get(pk=line_id)

        if shift_date.weekday() <= 4:
            shift_day = "WD"
        elif shift_date.weekday() == 5:
            shift_day = "SAT"
        elif shift_date.weekday() == 6:
            shift_day = "SUN"
        shifts_on_line = ShiftOnLine.objects.filter(line_id=line_id, shift_time__day=shift_day)

        vehicles = Vehicle.objects.filter(model__type__line=line)
        drivers = Driver.objects.all()
        return render(request, 'add_shift_line_date.html', {'line_id': line_id,
                                                            'shift_date': shift_date,
                                                            'line': line,
                                                            'shift_day': shift_day,
                                                            'shifts_on_line': shifts_on_line,
                                                            'vehicles': vehicles,
                                                            'drivers': drivers})

    def post(self, request, line_id, shift_date):
        shift_day = request.POST['shift_day']
        shift_daytime = request.POST['shift_daytime']
        shift_time = ShiftTime.objects.get(day=shift_day, daytime=shift_daytime)
        shift_on_line = ShiftOnLine.objects.get(line_id=line_id, shift_time=shift_time)

        shift_number = request.POST['shift_number']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        vehicle_id = request.POST['vehicle_id']
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        driver_id = request.POST['driver_id']
        driver = Driver.objects.get(pk=driver_id)
        Shift(date=shift_date, shift_on_line=shift_on_line, shift_number=shift_number,
              start_time=start_time, end_time=end_time, vehicle=vehicle, driver=driver).save()
        return redirect(f'/shifts/{line_id}/{shift_date}')


class EditShiftView(LoginRequiredMixin, View):
    def get(self, request, shift_id):
        header = "Edit Shift"

        shift = Shift.objects.get(pk=shift_id)
        form = EditShiftForm(instance=shift)
        return render(request, 'form.html', {'form': form, 'header': header})

    def post(self, request, shift_id):
        header = "Edit Shift"

        shift = Shift.objects.get(pk=shift_id)
        form = EditShiftForm(request.POST, instance=shift)

        if form.is_valid():
            form.save()
            return redirect('shifts_on_line',
                            line_id=shift.shift_on_line.line.id,
                            shift_date=shift.date)
        return render(request, 'form.html', {'form': form, 'header': header})


class DeleteShiftView(LoginRequiredMixin, View):
    def get(self, request, shift_id):
        shift = Shift.objects.get(pk=shift_id)
        line_id = shift.shift_on_line.line.id
        shift_date = shift.date
        shift.delete()
        return redirect('shifts_on_line',
                        line_id=line_id,
                        shift_date=shift_date)


class VehiclesView(View):
    def get(self, request):
        vehicles = Vehicle.objects.all().order_by('side_number')
        return render(request, 'vehicles.html', {'vehicles': vehicles})


class AddVehicleView(LoginRequiredMixin, View):
    def get(self, request):
        header = "Add Vehicle"

        form = VehicleForm()
        return render(request, 'form.html', {'form': form, 'header': header})

    def post(self, request):
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicles')
        else:
            header = "Add Vehicle"
            return render(request, 'form.html', {'form': form, 'header': header})


class EditVehicleView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        header = "Edit Vehicle"

        vehicle = Vehicle.objects.get(pk=vehicle_id)
        form = VehicleForm(instance=vehicle)
        return render(request, 'form.html', {'form': form, 'header': header})

    def post(self, request, vehicle_id):
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicles')
        else:
            header = "Edit Vehicle"
            return render(request, 'form.html', {'form': form, 'header': header})


class DeleteVehicleView(LoginRequiredMixin, View):
    def get(self, request, vehicle_id):
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        vehicle.delete()
        return redirect('vehicles')


class DriversView(LoginRequiredMixin, View):
    def get(self, request):
        drivers = Driver.objects.all()
        return render(request, 'drivers.html', {'drivers': drivers})


class AddDriverView(LoginRequiredMixin, View):
    def get(self, request):
        header = "Add driver"
        form = DriverForm()
        return render(request, 'form.html', {'form': form, 'header': header})

    def post(self, request):
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('drivers')
        else:
            header = "Add driver"
            return render(request, 'form.html', {'form': form, 'header': header})


class EditDriverView(LoginRequiredMixin, View):
    def get(self, request, driver_id):
        header = "Edit Driver"

        driver = Driver.objects.get(pk=driver_id)
        form = DriverForm(instance=driver)
        return render(request, 'form.html', {'form': form, 'header': header})

    def post(self, request, driver_id):
        header = "Edit Driver"

        driver = Driver.objects.get(pk=driver_id)
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('drivers')
        else:
            return render(request, 'form.html', {'form': form, 'header': header})


class DeleteDriverView(LoginRequiredMixin, View):
    def get(self, request, driver_id):
        driver = Driver.objects.get(pk=driver_id)
        driver.delete()
        return redirect('drivers')