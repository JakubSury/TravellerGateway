from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from .models import Expense, ToDo, Like, Trip


class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['title', 'start_date', 'end_date', 'description', 'countries']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('trip', args=(self.object.id,))


class TripUpdateView(UpdateView):
    model = Trip
    fields = "__all__"

    def get_success_url(self):
        return reverse('trip', args=(self.object.id, ))


class TripsListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'blog/trips.html'
    context_object_name = 'trips'

    def get_queryset(self):
        return Trip.objects.filter(author=self.request.user)


def home_view(request):
    if request.user.is_authenticated:
        other_trips = Trip.objects.exclude(author=request.user)
        for trip in other_trips:
            trip.user_has_liked = trip.like_set.filter(user=request.user).exists()
    else:
        other_trips = Trip.objects.none()
    context = {'other_trips': other_trips}
    return render(request, 'blog/home.html', context)


def like_trip(request, trip_id):
    if request.method == 'POST':
        trip = Trip.objects.get(pk=trip_id)
        user = request.user
        if Like.objects.filter(user=user, trip=trip).exists():
            Like.objects.filter(user=user, trip=trip).delete()
        else:
            Like.objects.create(user=user, trip=trip)
    return redirect('home')


def liked_trips_view(request):
    liked_trips = Like.objects.filter(user=request.user)
    context = {
        'liked_trips': liked_trips
    }
    return render(request, 'blog/liked_trips.html', context)


def unlike_trip_view(request, trip_id):
    like = get_object_or_404(Like, user=request.user, trip_id=trip_id)
    like.delete()
    return redirect('liked_trips')


def user_signup_view(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = forms.SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def user_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Nieprawidłowa nazwa użytkownika lub hasło."
            return render(request, 'blog/login.html', {'error_message': error_message})
    else:
        return render(request, 'blog/login.html')


def user_logout_view(request):
    logout(request)
    return redirect('home')


def trip_detail_view(request, pk):

    trip = get_object_or_404(Trip, id=pk)
    if request.user._get_pk_val() == trip.author.pk:
        expenses = trip.expenses.all()
        todos = trip.to_dos.all()
    else:
        expenses = trip.expenses.none()
        todos = trip.to_dos.none()
    total_planned_cost = sum(expense.planned_cost for expense in expenses)
    total_actual_cost = sum(expense.actual_cost for expense in expenses)
    ctx = {
        'trip': trip,
        'expenses': expenses,
        'total_planned_cost': total_planned_cost,
        'total_actual_cost': total_actual_cost,
        'todos': todos
    }
    return render(request, 'blog/trip_detail.html', ctx)


def expense_create(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    if request.method == 'POST':
        form = forms.ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.trip = trip
            expense.save()
            trip.expenses.add(expense)
            return redirect('trip', pk=trip_id)
    else:
        form = forms.ExpenseForm()
    return render(request, 'blog/expense_form.html', {'form': form})


def expense_update(request, trip_id, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if request.method == 'POST':
        form = forms.ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('trip', pk=trip_id)
    else:
        form = forms.ExpenseForm(instance=expense)
    return render(request, 'blog/expense_form.html', {'form': form})


def expense_delete(request, trip_id, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('trip', pk=trip_id)
    return render(request, 'blog/expense_confirm_delete.html', {'expense': expense})


def todo_create(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        form = forms.ToDoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.trip = trip
            todo.save()
            trip.to_dos.add(todo)
            return redirect('trip', pk=trip_id)
    else:
        form = forms.ToDoForm()
    return render(request, 'blog/todo_form.html', {'form': form})


def todo_update(request, trip_id, todo_id):
    todo = get_object_or_404(ToDo, pk=todo_id)
    if request.method == 'POST':
        form = forms.ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('trip', pk=trip_id)
    else:
        form = forms.ToDoForm(instance=todo)
    return render(request, 'blog/todo_form.html', {'form': form})


def todo_delete(request, trip_id, todo_id):
    todo = get_object_or_404(ToDo, pk=todo_id)
    if request.method == 'POST':
        todo.delete()
        return redirect('trip', pk=trip_id)
    return render(request, 'blog/todo_confirm_delete.html', {'todo': todo})

