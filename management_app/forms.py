from django import forms

from management_app.models import Shift, Vehicle, Driver, Line, ShiftOnLine


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}),
                               required=False)


class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        fields = '__all__'
        widgets = {
            'vehicle_type': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class EditShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        exclude = ['overtime']
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d',
                                    attrs={'class': 'form-control', 'type': 'date', 'readonly': 'readonly'}),
            'shift_on_line': forms.Select(attrs={'readonly': 'readonly'}),
            'start_time': forms.TimeInput(format='%H:%M',
                                          attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(format='%H:%M',
                                        attrs={'class': 'form-control', 'type': 'time'}),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'production_date': forms.DateInput(format='%Y-%m-%d',
                                               attrs={'class': 'form-control', 'type': 'date'}),
            'last_review': forms.DateInput(format='%Y-%m-%d',
                                           attrs={'class': 'form-control', 'type': 'date'}),
            'next_review': forms.DateInput(format='%Y-%m-%d',
                                           attrs={'class': 'form-control', 'type': 'date'}),
        }


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'license_validity': forms.DateInput(format='%Y-%m-%d',
                                                attrs={'class': 'form-control', 'type': 'date'}),
            'vehicle_assigned': forms.Select(attrs={'class': 'form-control'}),
        }