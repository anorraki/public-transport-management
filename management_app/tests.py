import pytest
from django.test import TestCase, Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from management_app.conftest import vehicle_type
from management_app.forms import LoginForm, LineForm, EditShiftForm, VehicleForm, DriverForm
from management_app.models import Line, ShiftOnLine, Shift, Vehicle, Driver


# Create your tests here.


def test_index():
    client = Client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, LoginForm)


@pytest.mark.django_db
def test_login_post(user):
    client = Client()
    url = reverse('index')
    data = {
        'username': user.username,
        'password': 'pass'
    }
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout(user):
    client = Client()
    client.force_login(user)
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_lines_get(lines):
    client = Client()
    url = reverse('lines')
    response = client.get(url)
    assert response.status_code == 200
    lines_from_view = response.context['lines']
    assert lines_from_view.count() == len(lines)


@pytest.mark.django_db
def test_add_line_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_line')
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, LineForm)
    header = response.context['header']
    assert header in str(response.content)


@pytest.mark.django_db
def test_add_line_post(user, vehicle_type):
    client = Client()
    client.force_login(user)
    url = reverse('add_line')
    data = dict(name='line', distance=5, first_stop='a', last_stop='a')
    response = client.post(url, data)
    assert response.status_code == 302
    assert Line.objects.get(name='line', distance=5, first_stop='a', last_stop='a')


@pytest.mark.django_db
def test_edit_line_get(user, line):
    client = Client()
    client.force_login(user)
    url = reverse('edit_line', args=(line.id,))
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, LineForm)
    header = response.context['header']
    assert header in str(response.content)


@pytest.mark.django_db
def test_edit_line_post(user, line):
    client = Client()
    client.force_login(user)
    url = reverse('edit_line', args=(line.id,))
    data = dict(name=line.name, distance=line.distance,
                first_stop=line.first_stop, last_stop=line.last_stop)
    response = client.post(url, data)
    assert response.status_code == 302
    assert Line.objects.get(name=line.name, distance=line.distance,
                            first_stop=line.first_stop, last_stop=line.last_stop)
    url = reverse('lines')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_delete_line_get(user, line):
    client = Client()
    client.force_login(user)
    url = reverse('delete_line', args=(line.id,))
    response = client.get(url)
    assert line.delete()
    assert response.status_code == 302


@pytest.mark.django_db
def test_line_shift_detail_get(user, shifts_on_line, line):
    client = Client()
    line = shifts_on_line[0].line
    url = reverse('line_shift', args=(line.id,))
    response = client.get(url)
    assert response.status_code == 200
    shifts_on_line_from_view = response.context['shift_on_line']
    assert shifts_on_line_from_view.count() == len(shifts_on_line)
    line_from_view = response.context['line']
    assert line_from_view.name in str(response.content)


@pytest.mark.django_db
def test_add_line_shift_get(user, line, shift_times):
    client = Client()
    client.force_login(user)
    url = reverse('add_line_shift', args=(line.id,))
    response = client.get(url)
    assert response.status_code == 200
    line_from_view = response.context['line']
    assert line_from_view.name in str(response.content)
    shift_time_from_view = response.context['shift_time']
    assert shift_time_from_view.count() == len(shift_times)


@pytest.mark.django_db
def test_add_line_shift_post(user, line, shift_time):
    client = Client()
    client.force_login(user)
    url = reverse('add_line_shift', args=(line.id,))
    data = dict(line=line.id, shift_time=shift_time.id, number_of_shifts=1)
    response = client.post(url, data)
    assert response.status_code == 302
    assert ShiftOnLine.objects.get(line=line, shift_time=shift_time, number_of_shifts=1)
    url_res = f'/line/shifts/{line.id}'
    assert response.url.startswith(url_res)


@pytest.mark.django_db
def test_edit_line_shift_get(user, line, shift_on_line):
    client = Client()
    client.force_login(user)
    url = reverse('edit_line_shift', args=(line.id, shift_on_line.id,))
    response = client.get(url)
    assert response.status_code == 200
    line = response.context['line']
    assert line.name in str(response.content)


@pytest.mark.django_db
def test_edit_line_shift_post(user, line, shift_on_line, shift_time):
    client = Client()
    client.force_login(user)
    url = reverse('edit_line_shift', args=(line.id, shift_on_line.id,))
    data = dict(line=line.id, shift_time=shift_time.id, number_of_shifts=1)
    response = client.post(url, data)
    assert response.status_code == 302
    assert ShiftOnLine.objects.get(line=line, shift_time=shift_time, number_of_shifts=1)
    url = f'/line/shifts/{line.id}'
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_delete_line_shift_get(user, line, shift_on_line, shift_time):
    client = Client()
    client.force_login(user)
    url = reverse('delete_line_shift', args=(line.id, shift_on_line.id,))
    response = client.get(url)
    assert shift_on_line.delete()
    assert response.status_code == 302


@pytest.mark.django_db
def test_shifts_on_lines_get(user, lines, shifts_on_line):
    client = Client()
    url = reverse('shifts')
    response = client.get(url)
    assert response.status_code == 200
    lines_from_view = response.context['lines']
    assert lines_from_view.count() == len(lines)
    shifts_on_line_from_view = response.context['shift_line']
    assert shifts_on_line_from_view.count() == len(shifts_on_line)


@pytest.mark.django_db
def test_shifts_on_lines_detail_get(lines):
    client = Client()
    shift_date = '2222-01-01'
    url = f'/shifts/{lines[0].id}/{shift_date}'
    response = client.get(url)
    assert response.status_code == 200
    lines_from_view = response.context['all_lines']
    assert lines_from_view.count() == len(lines)


@pytest.mark.django_db
def test_shifts_on_lines_detail_post(user, lines):
    client = Client()
    client.force_login(user)
    shift_date = '2222-01-01'
    url = f'/shifts/{lines[0].id}/{shift_date}'
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_shift_line_date_get(user, line, drivers):
    client = Client()
    client.force_login(user)
    shift_date = '2222-01-01'
    url = f'/add-shift/{line.id}/{shift_date}'
    response = client.get(url)
    assert response.status_code == 200
    drivers_from_view = response.context['drivers']
    assert drivers_from_view.count() == len(drivers)


# @pytest.mark.django_db
# def test_add_shift_line_date_post(user, line, shift, vehicle, driver):
#     client = Client()
#     client.force_login(user)
#     shift_date = '2222-01-01'
#     url = f'/add-shifts/{line.id}/{shift_date}'
#     data = dict(date=shift_date, shift_number=1, start_time='6:00',
#                 end_time='7:00', overtime='1:00', vehicles=vehicle.id, drivers=driver.id)
#     response = client.post(url, data)
#     assert response.status_code == 302
#     # Shift.objects.create(date='2222-01-01', shift_number=x, start_time='6:00',
#     #                      end_time='7:00', overtime='2:00'))


@pytest.mark.django_db
def test_edit_shift_get(user, shifts, drivers):
    client = Client()
    client.force_login(user)
    url = reverse('edit_shift_line_date', args=(shifts[0].id,))
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, EditShiftForm)
    header = response.context['header']
    assert header in str(response.content)


@pytest.mark.django_db
def test_edit_shift_post(user, shift, driver, vehicle):
    client = Client()
    client.force_login(user)
    url = reverse('edit_shift_line_date', args=(shift.id,))
    data = dict(date='2222-01-01', shift_number=1, start_time='6:00',
                end_time='7:00', overtime='2:00', driver=driver.id, vehicle=vehicle.id)
    response = client.post(url, data)
    assert response.status_code == 200
    assert Shift.objects.get(date='2222-01-01', shift_number=1, start_time='6:00',
                             end_time='7:00', overtime='2:00', driver=driver, vehicle=vehicle)


@pytest.mark.django_db
def test_delete_shift_get(user, lines, shifts):
    client = Client()
    client.force_login(user)
    shift_date = '2222-01-01'
    url = f'/shifts/{lines[0].id}/{shift_date}'
    response = client.get(url)
    assert shifts[0].delete()
    assert response.status_code == 200


@pytest.mark.django_db
def test_vehicles_get(user, vehicles):
    client = Client()
    url = reverse('vehicles')
    response = client.get(url)
    assert response.status_code == 200
    vehicles_from_view = response.context['vehicles']
    assert vehicles_from_view.count() == len(vehicles)


@pytest.mark.django_db
def test_add_vehicle_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_vehicle')
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, VehicleForm)
    header = response.context['header']
    assert header in str(response.content)


@pytest.mark.django_db
def test_add_vehicle_post(user, vehicle_model):
    client = Client()
    client.force_login(user)
    url = reverse('add_vehicle')
    data = dict(side_number=1, model=vehicle_model.id, plate=1, production_date='2222-01-01',
                last_review='2222-01-01', next_review='2222-01-01')
    response = client.post(url, data)
    assert response.status_code == 302
    assert Vehicle.objects.get(side_number=1, model=vehicle_model, plate=1, production_date='2222-01-01',
                               last_review='2222-01-01', next_review='2222-01-01')


@pytest.mark.django_db
def test_edit_vehicle_get(user, vehicle):
    client = Client()
    client.force_login(user)
    url = reverse('edit_vehicle', args=(vehicle.id,))
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, VehicleForm)
    header = response.context['header']
    assert header in str(response.content)


@pytest.mark.django_db
def test_edit_vehicle_post(user, vehicle, vehicle_model):
    client = Client()
    client.force_login(user)
    url = reverse('edit_vehicle', args=(vehicle.id,))
    data = dict(side_number=1, model=vehicle_model.id, plate=1, production_date='2222-01-01',
                last_review='2222-01-01', next_review='2222-01-01')
    response = client.post(url, data)
    assert response.status_code == 302
    assert Vehicle.objects.get(side_number=1, model=vehicle_model, plate=1, production_date='2222-01-01',
                               last_review='2222-01-01', next_review='2222-01-01')


@pytest.mark.django_db
def test_delete_vehicle_get(user, vehicle):
    client = Client()
    client.force_login(user)
    url = reverse('delete_vehicle', args=(vehicle.id, ))
    response = client.get(url)
    assert vehicle.delete()
    assert response.status_code == 302


@pytest.mark.django_db
def test_drivers_get(user, drivers):
    client = Client()
    client.force_login(user)
    url = reverse('drivers')
    response = client.get(url)
    assert response.status_code == 200
    drivers_from_view = response.context['drivers']
    assert drivers_from_view.count() == len(drivers)


@pytest.mark.django_db
def test_add_driver_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_driver')
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, DriverForm)
    header = response.context['header']
    assert header in str(response.content)


@pytest.mark.django_db
def test_add_driver_post(user, employee, vehicle, vehicle_model):
    client = Client()
    client.force_login(user)
    url = reverse('add_driver')
    data = dict(employee=employee.id, license_validity='2222-01-01', vehicle_assigned=vehicle.id)
    response = client.post(url, data)
    assert response.status_code == 302
    assert Driver.objects.get(employee=employee, license_validity='2222-01-01', vehicle_assigned=vehicle)



@pytest.mark.django_db
def test_edit_driver_get(user, driver):
    client = Client()
    client.force_login(user)
    url = reverse('edit_driver', args=(driver.id,))
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context['form']
    assert isinstance(form_in_view, DriverForm)
    header = response.context['header']
    assert header in str(response.content)


@pytest.mark.django_db
def test_edit_driver_post(user, driver, employee, vehicle):
    client = Client()
    client.force_login(user)
    url = reverse('edit_driver', args=(driver.id,))
    data = dict(employee=employee.id, license_validity='2222-01-01', vehicle_assigned=vehicle.id)
    response = client.post(url, data)
    assert response.status_code == 302
    assert Driver.objects.get(employee=employee, license_validity='2222-01-01', vehicle_assigned=vehicle)


@pytest.mark.django_db
def test_delete_vehicle_get(user, driver):
    client = Client()
    client.force_login(user)
    url = reverse('delete_driver', args=(driver.id, ))
    response = client.get(url)
    assert driver.delete()
    assert response.status_code == 302
