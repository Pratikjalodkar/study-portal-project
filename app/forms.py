from django import forms
from .models import Notes, Homework, Todo
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label='Search here:')


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']

class ConversionForm(forms.Form):
    Choices = [('length','length'),('mass','mass'),
            #    ('temperature','temperature'),('currency','currency')
               ]
    measurement = forms.ChoiceField(choices=Choices, widget= forms.RadioSelect)
    # from_currency = forms.CharField(max_length=3, label='From Currency')
    # to_currency = forms.CharField(max_length=3, label='To Currency')
    # amount = forms.FloatField(label='Amount')
    # result = forms.FloatField(label='Result', disabled=True)
    # date = forms.DateField(label='Date', disabled=True)
    # rate = forms.FloatField(label='Rate', disabled=True)
    # rate_date = forms.DateField(label='Rate Date', disabled=True)




class ConversionLengthForm(forms.Form):
    Choices = [('yards', 'Yards'), ('foot', 'foot'), 
            #    ('meters', 'meters'), ('kilometers', 'kilometers'),
            #    ('centimeters','centimeters'),('millimeters','millimeters'),
            #    ('micrometers','micrometers'),('nanometers','nanometers'),
            #    ('miles','miles'),
            #    ('inches','inches'),
            #    ('nautical_miles','nautical_miles')
               ]
    input = forms.CharField(required = False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the Number'}))
    measure1 = forms.CharField(
        label='',widget=forms.Select(choices=Choices)
    )
    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=Choices)
    )



class ConversionMassForm(forms.Form):
    Choices = [('pound', 'Pound'), ('kilogram', 'Kilogram'),]
    input = forms.CharField(required = False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the Number'}))
    measure1 = forms.CharField(
        label='',widget=forms.Select(choices=Choices)
    )
    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=Choices)
    )

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = []










