"""PublicTransportCompany URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, register_converter

from management_app import views
from management_app.coverters import DateConverter

register_converter(DateConverter, 'date')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('lines/', views.LinesView.as_view(), name='lines'),
    path('lines/add-line', views.AddLineView.as_view(), name='add_line'),
    path('line/<int:line_id>/edit/', views.EditLineView.as_view(), name='edit_line'),
    path('line/<int:line_id>/delete/', views.DeleteLineView.as_view(), name='delete_line'),

    path('shifts/', views.ShiftsOnLinesView.as_view(), name='shifts'),
    path('shifts/<int:line_id>/<date:shift_date>', views.ShiftsOnLineDetailView.as_view(), name='shifts_on_line'),
    path('add-shift/<int:line_id>/<date:shift_date>', views.AddShiftLineDateView.as_view(), name='add_shift_line_date'),
    path('shifts/<int:shift_id>/edit/', views.EditShiftView.as_view(), name='edit_shift_line_date'),
    path('shifts/<int:shift_id>/delete/', views.DeleteShiftView.as_view(), name='delete_shift_line_date'),

    path('line/shifts/<int:line_id>/', views.LineShiftDetailView.as_view(), name='line_shift'),
    path('line/shifts/<int:line_id>/add-shift', views.AddLineShiftView.as_view(), name='add_line_shift'),
    path('line/shifts/<int:line_id>/<int:shift_id>/edit', views.EditLineShiftView.as_view(), name='edit_line_shift'),
    path('line/shifts/<int:line_id>/<int:shift_id>/delete',
         views.DeleteLineShiftView.as_view(), name='delete_line_shift'),

    path('vehicles/', views.VehiclesView.as_view(), name='vehicles'),
    path('vehicles/add-vehicle', views.AddVehicleView.as_view(), name='add_vehicle'),
    path('vehicle/<int:vehicle_id>/edit/', views.EditVehicleView.as_view(), name='edit_vehicle'),
    path('vehicle/<int:vehicle_id>/delete/', views.DeleteVehicleView.as_view(), name='delete_vehicle'),

    path('drivers/', views.DriversView.as_view(), name='drivers'),
    path('drivers/add-driver', views.AddDriverView.as_view(), name='add_driver'),
    path('driver/<int:driver_id>/edit/', views.EditDriverView.as_view(), name='edit_driver'),
    path('driver/<int:driver_id>/delete/', views.DeleteDriverView.as_view(), name='delete_driver'),

]
