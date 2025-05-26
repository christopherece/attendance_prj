from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import csv
import json

from visitor.models import Attendance, Child, Teacher

# Authentication views
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

# Teacher management views
@login_required(login_url='admin_login')
def add_teacher(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        class_name = request.POST.get('class_name')
        
        teacher = Teacher.objects.create(
            name=name,
            email=email,
            class_name=class_name
        )
        
        messages.success(request, 'Teacher added successfully')
        return redirect('admin_teacher_list')
    
    return render(request, 'admin_portal/add_teacher.html')

@login_required(login_url='admin_login')
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        teacher.name = request.POST.get('name')
        teacher.email = request.POST.get('email')
        teacher.class_name = request.POST.get('class_name')
        teacher.save()
        
        messages.success(request, 'Teacher updated successfully')
        return redirect('admin_teacher_list')
    
    return render(request, 'admin_portal/edit_teacher.html', {'teacher': teacher})

@login_required(login_url='admin_login')
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    messages.success(request, 'Teacher deleted successfully')
    return redirect('admin_teacher_list')

# Authentication views
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'admin_portal/login.html')

@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Dashboard view
@login_required(login_url='admin_login')
def index(request):
    # Get total number of check-ins today
    today = datetime.now().date()
    today_checkins = Attendance.objects.filter(check_in_time__date=today).count()

    # Get number of unique children checked in today
    unique_today_checkins = Attendance.objects.filter(check_in_time__date=today).values('child').distinct().count()

    # Get total number of check-ins in the last 7 days
    last_week = datetime.now() - timedelta(days=7)
    last_week_checkins = Attendance.objects.filter(check_in_time__gte=last_week).count()

    # Get number of unique children checked in in the last 7 days
    unique_last_week_checkins = Attendance.objects.filter(check_in_time__gte=last_week).values('child').distinct().count()

    # Get top 5 most attended children
    top_attended = Child.objects.annotate(
        attendance_count=Count('attendance')
    ).order_by('-attendance_count')[:5]

    # Get check-in count per hour for the last 24 hours
    last_24_hours = datetime.now() - timedelta(hours=24)
    hourly_stats = Attendance.objects.filter(
        check_in_time__gte=last_24_hours
    ).extra(
        select={'hour': 'strftime("%H", check_in_time)'}
    ).values('hour').annotate(
        count=Count('id')
    ).order_by('hour')

    # Prepare data for the charts
    labels = [f"{h}:00" for h in range(24)]
    data = [0] * 24
    for stat in hourly_stats:
        data[int(stat['hour'])] = stat['count']

    context = {
        'today_checkins': today_checkins,
        'unique_today_checkins': unique_today_checkins,
        'last_week_checkins': last_week_checkins,
        'unique_last_week_checkins': unique_last_week_checkins,
        'top_attended': top_attended,
        'labels': labels,
        'data': data,
    }

    return render(request, 'admin_portal/index.html', context)

@login_required(login_url='admin_login')
def get_realtime_stats(request):
    """
    Get real-time attendance statistics
    """
    from datetime import datetime, timedelta
    
    # Get total number of check-ins today
    today = datetime.now().date()
    today_checkins = Attendance.objects.filter(check_in_time__date=today).count()
    
    # Get number of currently checked-in children
    currently_checked_in = Attendance.objects.filter(is_checked_in=True).count()
    
    # Get check-in count per hour for the last 24 hours
    last_24_hours = datetime.now() - timedelta(hours=24)
    hourly_stats = Attendance.objects.filter(
        check_in_time__gte=last_24_hours
    ).extra(
        select={'hour': 'strftime("%H", check_in_time)'}
    ).values('hour').annotate(
        count=Count('id')
    ).order_by('hour')
    
    # Prepare data for the charts
    labels = [f"{h}:00" for h in range(24)]
    data = [0] * 24
    for stat in hourly_stats:
        data[int(stat['hour'])] = stat['count']
    
    return JsonResponse({
        'today_checkins': today_checkins,
        'currently_checked_in': currently_checked_in,
        'labels': labels,
        'data': data,
    })

# Visitor management views
@login_required(login_url='admin_login')
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-check_in_time')
    return render(request, 'admin_portal/attendance_list.html', {'attendances': attendances})

@login_required(login_url='admin_login')
def export_attendances(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendances.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Child', 'Check-in Time', 'Check-out Time', 'Status'])
    
    attendances = Attendance.objects.all().order_by('-check_in_time')
    for attendance in attendances:
        status = 'Checked In' if attendance.is_checked_in else 'Checked Out'
        writer.writerow([attendance.child.name, attendance.check_in_time, attendance.check_out_time, status])
    
    return response

# Staff management views
@login_required(login_url='admin_login')
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'admin_portal/teacher_list.html', {'teachers': teachers})
def staff_list(request):
    staff = PersonToVisit.objects.all()
    return render(request, 'admin_portal/staff_list.html', {'staff': staff})

@login_required(login_url='admin_login')
def add_staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        if name and email:
            PersonToVisit.objects.create(name=name, email=email)
            messages.success(request, 'Staff member added successfully')
            return redirect('admin_staff_list')
        else:
            messages.error(request, 'Please provide both name and email')
    
    return render(request, 'admin_portal/staff_form.html')

@login_required(login_url='admin_login')
def edit_staff(request, staff_id):
    staff = get_object_or_404(PersonToVisit, id=staff_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        if name and email:
            staff.name = name
            staff.email = email
            staff.save()
            messages.success(request, 'Staff member updated successfully')
            return redirect('admin_staff_list')
        else:
            messages.error(request, 'Please provide both name and email')
    
    return render(request, 'admin_portal/staff_form.html', {'staff': staff})

@login_required(login_url='admin_login')
def delete_staff(request, staff_id):
    staff = get_object_or_404(PersonToVisit, id=staff_id)
    
    if request.method == 'POST':
        staff.delete()
        messages.success(request, 'Staff member deleted successfully')
        return redirect('admin_staff_list')
    
    return render(request, 'admin_portal/staff_confirm_delete.html', {'staff': staff})

# Reporting views
@login_required(login_url='admin_login')
def daily_report(request):
    selected_date = request.GET.get('date', timezone.now().date().strftime('%Y-%m-%d'))
    try:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        date_obj = timezone.now().date()
    
    visitors = Visitor.objects.filter(login_date__date=date_obj).order_by('login_date')
    
    # Get hourly distribution
    hours = range(0, 24)
    hourly_counts = []
    
    for hour in hours:
        count = visitors.filter(login_date__hour=hour).count()
        hourly_counts.append(count)
    
    context = {
        'selected_date': selected_date,
        'visitors': visitors,
        'total_visitors': visitors.count(),
        'hours': json.dumps(list(hours)),
        'hourly_counts': json.dumps(hourly_counts)
    }
    
    return render(request, 'admin_portal/daily_report.html', context)

@login_required(login_url='admin_login')
def weekly_report(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    visitors = Visitor.objects.filter(
        login_date__date__gte=start_of_week,
        login_date__date__lte=end_of_week
    ).order_by('login_date')
    
    # Get daily distribution
    days = [start_of_week + timedelta(days=i) for i in range(7)]
    day_names = [day.strftime('%A') for day in days]
    daily_counts = []
    
    for day in days:
        count = visitors.filter(login_date__date=day).count()
        daily_counts.append(count)
    
    context = {
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'visitors': visitors,
        'total_visitors': visitors.count(),
        'day_names': json.dumps(day_names),
        'daily_counts': json.dumps(daily_counts)
    }
    
    return render(request, 'admin_portal/weekly_report.html', context)

@login_required(login_url='admin_login')
def monthly_report(request):
    today = timezone.now().date()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    # Get first and last day of the month
    first_day = datetime(year, month, 1).date()
    if month == 12:
        last_day = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1).date() - timedelta(days=1)
    
    visitors = Visitor.objects.filter(
        login_date__date__gte=first_day,
        login_date__date__lte=last_day
    ).order_by('login_date')
    
    # Get daily distribution
    days_in_month = (last_day - first_day).days + 1
    days = [first_day + timedelta(days=i) for i in range(days_in_month)]
    day_numbers = [day.day for day in days]
    daily_counts = []
    
    for day in days:
        count = visitors.filter(login_date__date=day).count()
        daily_counts.append(count)
    
    # Get staff distribution
    staff_visits = PersonToVisit.objects.filter(
        visitor__login_date__date__gte=first_day,
        visitor__login_date__date__lte=last_day
    ).annotate(visit_count=Count('visitor')).order_by('-visit_count')
    
    staff_names = [staff.name for staff in staff_visits[:10]]  # Top 10 staff
    staff_counts = [staff.visit_count for staff in staff_visits[:10]]
    
    context = {
        'year': year,
        'month': month,
        'month_name': first_day.strftime('%B'),
        'visitors': visitors,
        'total_visitors': visitors.count(),
        'day_numbers': json.dumps(day_numbers),
        'daily_counts': json.dumps(daily_counts),
        'staff_names': json.dumps(staff_names),
        'staff_counts': json.dumps(staff_counts)
    }
    
    return render(request, 'admin_portal/monthly_report.html', context)

@login_required(login_url='admin_login')
def custom_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            visitors = Visitor.objects.filter(
                login_date__date__gte=start_date_obj,
                login_date__date__lte=end_date_obj
            ).order_by('login_date')
            
            # Get staff distribution
            staff_visits = PersonToVisit.objects.filter(
                visitor__login_date__date__gte=start_date_obj,
                visitor__login_date__date__lte=end_date_obj
            ).annotate(visit_count=Count('visitor')).order_by('-visit_count')
            
            staff_names = [staff.name for staff in staff_visits[:10]]  # Top 10 staff
            staff_counts = [staff.visit_count for staff in staff_visits[:10]]
            
            context = {
                'start_date': start_date,
                'end_date': end_date,
                'visitors': visitors,
                'total_visitors': visitors.count(),
                'staff_names': json.dumps(staff_names),
                'staff_counts': json.dumps(staff_counts),
                'has_data': True
            }
        except ValueError:
            context = {'has_data': False}
    else:
        context = {'has_data': False}
    
    return render(request, 'admin_portal/custom_report.html', context)
