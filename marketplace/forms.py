from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'price', 'condition', 'location', 'brand', 'quantity', 'negotiable')
        widgets = {'description': forms.Textarea(attrs={'rows': 6}), 'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})}


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Choose a unique username for your MarketGo account.'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    phone = forms.CharField(max_length=30)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, label='Your name')
    email = forms.EmailField(label='Email address')
    topic = forms.ChoiceField(choices=[
        ('buying', 'Buying a product'),
        ('selling', 'Selling a product'),
        ('listing', 'Report a listing'),
        ('account', 'Account help'),
        ('other', 'Something else'),
    ], label='What can we help with?')
    reference = forms.CharField(max_length=120, required=False, label='Order or listing reference')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 6}), max_length=2000)
