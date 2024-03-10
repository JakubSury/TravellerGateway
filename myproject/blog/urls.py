from django.urls import path, reverse_lazy
from . import views
from . import models

from django.views.generic import DeleteView


urlpatterns = [
    path('', views.home_view, name='home'),
    path('trips/', views.TripsListView.as_view(), name='trips'),

    path('liked-trips/', views.liked_trips_view, name='liked_trips'),
    path('like/<int:trip_id>/', views.like_trip, name='like_trip'),
    path('unlike/<int:trip_id>/', views.unlike_trip_view, name='unlike_trip'),

    path('login/', views.user_login_view, name='login'),
    path('logout/', views.user_logout_view, name='logout'),
    path('signup/', views.user_signup_view, name='signup'),

    path('trip/<int:pk>/', views.trip_detail_view, name='trip'),
    path('add-trip/', views.TripCreateView.as_view(), name='add_trip'),
    path('update-trip/<int:pk>/', views.TripUpdateView.as_view(), name='edit_trip'),
    path('delete-trip/<int:pk>/', DeleteView.as_view(model=models.Trip, success_url=reverse_lazy('trips')), name='delete_trip'),

    path('expense/create/<int:trip_id>/', views.expense_create, name='expense_create'),
    path('expense/update/<int:trip_id>/<int:expense_id>/', views.expense_update, name='expense_update'),
    path('expense/delete/<int:trip_id>/<int:expense_id>/', views.expense_delete, name='expense_delete'),

    path('todo/create/<int:trip_id>/', views.todo_create, name='todo_create'),
    path('todo/update/<int:trip_id>/<int:todo_id>/', views.todo_update, name='todo_update'),
    path('todo/delete/<int:trip_id>/<int:todo_id>/', views.todo_delete, name='todo_delete'),
]