from .models import Trip, Country, Expense, ToDo
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Wymagane. Podaj prawidłowy adres email.')
    username = forms.CharField(label='Nazwa użytkownika', max_length=150, help_text='Wymagane. Maksymalnie 150 znaków. Litery, cyfry i @/./+/-/_ tylko.')
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput, help_text='Wymagane. Hasło musi zawierać co najmniej 8 znaków.')
    password2 = forms.CharField(label='Potwierdź hasło', widget=forms.PasswordInput, help_text='Wprowadź to samo hasło, dla potwierdzenia.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TripForm(forms.ModelForm):
    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Kraje"
    )
    class Meta:
        model = Trip
        fields = ['title', 'start_date', 'end_date', 'description', 'countries']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'planned_cost', 'actual_cost']


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['task', 'status']