# Django
from django import forms

# Models
from opentrade.users.models import User
from opentrade.users.models import Profile
from opentrade.wallets.models import Wallet
from opentrade.portfolios.models import Portfolio


class SigninForm(forms.Form):

    username = forms.CharField(min_length=4, max_length=50)

    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )
    def clean_username(self):
        """Username must be valid"""
        username = self.cleaned_data['username']
        username_taken = not User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('username or password is incorrect.')
        return username

    def clean(self):
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')

        return data

class SignupForm(forms.Form):

    username = forms.CharField(
        min_length=4,
        max_length=50,
        widget=forms.TextInput()
    )

    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )

    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput()
    )

    currency = forms.CharField(
        max_length=3,
        min_length=3,
        required=True,
        widget=forms.Select()
    )

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use.')
        return username

    def clean(self):
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')
        print("--- PROFILE CLEANED ---")
        return data

    def save(self):
        print("--- PROFILE BEFORE SAVED ---")
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(
            username=data['username'], email=data['email'], password=data['password']
        )
        
        wallet = Wallet(40000.0, 40000.0)
        portfolio = Portfolio()
        wallet.save()
        portfolio.save()

        profile = Profile(
            user=user, 
            birthdate=data['birthdate'], 
            currency=data['currency'], 
            wallet=wallet,
            portfolio=portfolio
        )
        profile.save()
        print("--- PROFILE SAVED ---")