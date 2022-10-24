import pytest
from django.contrib.auth.models import User, Group
from django.utils.dateparse import parse_date, parse_time

from management_app.models import Line, VehicleType, ShiftOnLine, ShiftTime, Shift, Vehicle, VehicleModel, Driver, \
    Employee


@pytest.fixture
def user():
    return User.objects.create_user(username='user', password='pass')


@pytest.fixture
def group():
    return Group.objects.create(name='group')


@pytest.fixture
def employee(user, group):
    return Employee.objects.create(user=user, group=group, date_of_birth='2222-01-01', position='x',
                                   contract='FT', contract_start='2000-02-02', contract_end='2222-02-02')


@pytest.fixture
def lines():
    lst = []
    for x in range(10):
        lst.append(Line.objects.create(name=x, distance=x, first_stop=x, last_stop=x))
    return lst


@pytest.fixture
def vehicle_type():
    return VehicleType.objects.create(name='BUS', engine='D')


@pytest.fixture
def line():
    return Line.objects.create(name='a', distance=1, first_stop='a', last_stop='a')


@pytest.fixture
def shift_time():
    return ShiftTime.objects.create(day='WD', daytime='M', order=1)


@pytest.fixture
def shift_times():
    lst = []
    for x in range(10):
        lst.append(ShiftTime.objects.create(day=x, daytime=x, order=x))
    return lst


@pytest.fixture
def shifts_on_line(lines, shift_times):
    lst = []
    for x in range(20):
        lst.append(ShiftOnLine.objects.create(line=lines[0], shift_time=shift_times[0], number_of_shifts=x))
    return lst


@pytest.fixture
def shift_on_line(line, shift_time):
    return ShiftOnLine.objects.create(line=line, shift_time=shift_time, number_of_shifts=1)


@pytest.fixture
def vehicle_types():
    lst = []
    for x in range(20):
        lst.append(VehicleType.objects.create(name='BUS', engine='D'))
    return lst


@pytest.fixture
def models(vehicle_types):
    lst = []
    for x in range(20):
        lst.append(VehicleModel.objects.create(name=x, type=vehicle_types[0], capacity=x))
    return lst


@pytest.fixture
def vehicles(models):
    lst = []
    for x in range(20):
        lst.append(Vehicle.objects.create(side_number=x, model=models[0], plate=x, production_date='2222-01-01',
                                          last_review='2222-01-01', next_review='2222-01-01'))
    return lst


@pytest.fixture
def drivers(employee, vehicles):
    lst = []
    for x in range(1):
        lst.append(Driver.objects.create(employee=employee, license_validity='2222-01-01',
                                         vehicle_assigned=vehicles[0]))
    return lst


@pytest.fixture
def shifts():
    lst = []
    for x in range(20):
        lst.append(Shift.objects.create(date='2222-01-01', shift_number=x, start_time='6:00',
                                        end_time='7:00', overtime='2:00'))
        return lst


@pytest.fixture
def vehicle_type():
    return VehicleType.objects.create(name='BUS', engine='D')


@pytest.fixture
def vehicle_model(vehicle_type):
    return VehicleModel.objects.create(name='a', type=vehicle_type, capacity=1)


@pytest.fixture
def vehicle(vehicle_model):
    return Vehicle.objects.create(side_number=1, model=vehicle_model, plate=1, production_date='2222-01-01',
                                  last_review='2222-01-01', next_review='2222-01-01')


@pytest.fixture
def driver(employee, vehicle):
    return Driver.objects.create(employee=employee, license_validity='2222-01-01', vehicle_assigned=vehicle)


@pytest.fixture
def shift(shift_on_line, vehicle, driver):
    return Shift.objects.create(date='2222-01-01', shift_on_line=shift_on_line, shift_number=1, start_time='6:00',
                                end_time='7:00', overtime='2:00', vehicle=vehicle, driver=driver)

