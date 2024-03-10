from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa")
    alpha_2 = models.SlugField(max_length=2, unique=True, verbose_name="Kod alpha 2")

    class Meta:
        verbose_name = "Kraj"
        verbose_name_plural = "Kraje"
        ordering = ['name']

    def __str__(self):
        return self.name

class Expense(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa")
    planned_cost = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Planowany koszt")
    actual_cost = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Rzeczywisty koszt")

    class Meta:
        verbose_name = "Wydatek"
        verbose_name_plural = "Wydatki"

    def __str__(self):
        return self.name

class ToDo(models.Model):
    task = models.CharField(max_length=100, verbose_name="Zadanie")
    status = models.CharField(max_length=1, choices=( ('z', 'Zrobione'), ('n', 'Nie zrobione') ), default='n', verbose_name="Status")

    class Meta:
        verbose_name = "Do zrobienia"
        verbose_name_plural = "Do zrobienia"

    def __str__(self):
        return self.task

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"

    def __str__(self):
        return self.username
class SouvenirOffer(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tytuł")
    description = models.TextField( verbose_name="Opis")
    publication_date = models.DateField(verbose_name="Data publikacji", help_text="Data w formacie YYYY-MM-DD")
    availability = models.BooleanField(verbose_name="Dostępność", default=True)
    offered_or_wanted = models.CharField(max_length=1, choices=( ('o', 'Oferowane'), ('p', 'Poszukiwane') ), default='o')
    author = models.ForeignKey('blog.User', on_delete=models.PROTECT, verbose_name="Autor")
    origin_country = models.ForeignKey('blog.Country', on_delete=models.PROTECT, verbose_name="Kraj pochodzenia")

    class Meta:
        verbose_name = "Oferta pamiątki"
        verbose_name_plural = "Oferty pamiątek"

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey('blog.User', on_delete=models.PROTECT, verbose_name="Użytkownik")
    trip = models.ForeignKey('blog.Trip', on_delete=models.PROTECT, verbose_name="Wycieczka")

    class Meta:
        verbose_name = "Polubienie"
        verbose_name_plural = "Polubienia"

    def __str__(self):
        return f"{self.user} lubi {self.trip}"

class Trip(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tytuł")
    start_date = models.DateField(verbose_name="Data startu", help_text="Data w formacie YYYY-MM-DD")
    end_date = models.DateField(verbose_name="Data końca", help_text="Data w formacie YYYY-MM-DD")
    description = models.TextField( verbose_name="Opis")
    author = models.ForeignKey('blog.User', on_delete=models.PROTECT, verbose_name="Autor")
    countries = models.ManyToManyField('blog.Country', verbose_name="Kraje")
    expenses = models.ManyToManyField('blog.Expense', verbose_name="Wydatki", related_name='trips', blank=True)
    to_dos = models.ManyToManyField('blog.ToDo', verbose_name="Do zrobienia", related_name='trips', blank=True)

    class Meta:
        verbose_name = "Wycieczka"
        verbose_name_plural = "Wycieczki"

    def __str__(self):
        return self.description

class TravelProposal(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tytuł")
    description = models.TextField( verbose_name="Opis")
    publication_date = models.DateField(verbose_name="Data publikacji", help_text="Data w formacie YYYY-MM-DD")
    availability = models.BooleanField(verbose_name="Dostępność", default=True)
    countries = models.ManyToManyField('blog.Country', verbose_name="Kraje")
    author = models.ForeignKey('blog.User', on_delete=models.PROTECT, null=True, verbose_name="Autor")

    class Meta:
        verbose_name = "Propozycja podróży"
        verbose_name_plural = "Propozycje podróży"

    def __str__(self):
        return self.title