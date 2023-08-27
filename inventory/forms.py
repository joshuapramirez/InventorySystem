from django import forms
from django.forms import ModelForm, NumberInput
from .models import Inventory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxLengthValidator

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=15,
    )

    email = forms.EmailField(
        required=True,
        label='Email',
    )

    password1 = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        required=True,
        label='Confirm Password',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddProductForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].validators.append(MaxLengthValidator(15))
        self.fields['quantity_sold'].initial = 0

        self.fields['cost_per_item'].widget = NumberInput(attrs={'step': '0.01'})


        self.fields['cost_per_item'].validators.append(MinValueValidator(0))
        self.fields['quantity_in_stock'].validators.append(MinValueValidator(0))
        self.fields['quantity_sold'].validators.append(MinValueValidator(0))

class UpdateProductForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].validators.append(MaxLengthValidator(15))
        self.fields['cost_per_item'].widget = NumberInput(attrs={'step': '0.01'})

        self.fields['cost_per_item'].validators.append(MinValueValidator(0))
        self.fields['quantity_in_stock'].validators.append(MinValueValidator(0))
        self.fields['quantity_sold'].validators.append(MinValueValidator(0))