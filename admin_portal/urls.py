from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_dashboard'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('attendance/', views.attendance_list, name='admin_attendance_list'),
    path('attendance/export/', views.export_attendances, name='export_attendances'),
    path('teachers/', views.teacher_list, name='admin_teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/edit/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('teachers/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('reports/daily/', views.daily_report, name='daily_report'),
    path('reports/weekly/', views.weekly_report, name='weekly_report'),
    path('reports/monthly/', views.monthly_report, name='monthly_report'),
    path('reports/custom/', views.custom_report, name='custom_report'),
    path('stats/realtime/', views.get_realtime_stats, name='realtime_stats'),
]
