# visitor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/<int:attendance_id>/', views.check_out, name='check_out'),
    path('check-out-list/', views.check_out_list, name='check_out_list'),
    path('search-children/', views.search_children, name='search_children'),
    path('add-child/', views.add_child, name='add_child'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('search-staff/', views.search_staff, name='search_staff'),
]
