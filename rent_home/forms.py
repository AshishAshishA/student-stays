from django.forms import ModelForm
from django import forms
from .models import Room, House


class HouseForm(ModelForm):

    class Meta:
        model = House
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'latitude'  : forms.NumberInput(attrs={'id': 'lat', 'class':'input-field'}),
            'longitude' : forms.NumberInput(attrs={'id': 'long','class':'input-field'}),
            'house_no'  : forms.TextInput(attrs={'class':'input-field'}),
            'house_name': forms.TextInput(attrs={'class':'input-field'}),
            'owner_name': forms.TextInput(attrs={'class':'input-field'}),
            'contact_no': forms.NumberInput(attrs={'class':'input-field'}),
            'address'   : forms.Textarea(attrs={'class':'input-field', 'rows':4}),
            'area'      : forms.Select(attrs={'class':'input-field'}),
            'property_type': forms.Select(attrs={'class':'input-field'}),
            'image'     : forms.FileInput(attrs={'class':'input-field'})
        }




class RoomForm(ModelForm):

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['house']
        widgets = {
            'budget_range': forms.Select(attrs={'id': 'budget-range', 'class': 'input-field'}),
            'room_type': forms.Select(attrs={'class': 'input-field'}),
            'furnished': forms.CheckboxInput(attrs={'class': 'input-field'}),
            'available': forms.CheckboxInput(attrs={'class': 'input-field'}),
            'balcony': forms.CheckboxInput(attrs={'class': 'input-field'}),
            'lat_bath': forms.TextInput(attrs={'class': 'input-field'}),
            'rent': forms.TextInput(attrs={'class': 'input-field'}),
            'electricity_bill_per_unit': forms.TextInput(attrs={'class': 'input-field'}),
            'room_for': forms.Select(attrs={'class': 'input-field'}),
            'deposite_money': forms.TextInput(attrs={'class': 'input-field'}),
            'image': forms.FileInput(attrs={'class': 'input-field'}),
            
        }
