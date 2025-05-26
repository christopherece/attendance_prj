# visitor/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import AttendanceForm, ChildForm, TeacherForm
from .models import Attendance, Child, Teacher
from django.core.mail import send_mail
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


def logout(request, id):
    obj = get_object_or_404(Visitor, id=id)  # Use get_object_or_404 to handle not found cases
    
    if request.method == 'POST':
        
        obj.is_signin = False
        obj.signout_date = datetime.now()
        obj.save()
            
        # Store success message in session
        request.session['success_message'] = "Successfully logged out!"
        return redirect('login', permanent=False)
    
    return redirect('dashboard')
    

def signout_visitor(request):
    visitors = Visitor.objects.filter(is_signin=True).order_by('-login_date')
    context = {
        'visitors':visitors,
        'login_date':'login_date'
    }
    return render(request, 'visitor/signout.html', context)

def dashboard(request):
    today = datetime.now().date()
    today_attendances = Attendance.objects.filter(
        check_in_time__date=today
    ).order_by('-check_in_time')
    
    return render(request, 'visitor/dashboard.html', {
        'today_attendances': today_attendances
    })

def login(request):
    # Check if there's a success message in the session
    success_message = request.session.pop('success_message', None)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.check_in_time = datetime.now()
            attendance.is_checked_in = True
            attendance.save()
            
            # Send email notification to teacher
            if attendance.child.teacher and attendance.child.teacher.email:
                send_mail(
                    'Child Check-In Notification',
                    f'{attendance.child.name} has been checked in at {attendance.check_in_time}.',
                    'noreply@childcare.com',
                    [attendance.child.teacher.email],
                    fail_silently=True
                )
            
            messages.success(request, 'Child checked in successfully')
            return redirect('dashboard')
    else:
        form = AttendanceForm()
    
    children = Child.objects.all()
    
    return render(request, 'visitor/login.html', {
        'form': form,
        'success_message': success_message,
        'children': children
    })

def login_visitor(request):
    if request.method == 'POST':
        form = VisitorLoginForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            person_to_visit = form.cleaned_data['person_to_visit']
            staff_email = person_to_visit.email
            visitor, created = Visitor.objects.get_or_create(name=name, person_to_visit=person_to_visit)
            
            # Try to send email, but don't let SSL errors prevent login
            try:
                send_mail(
                    'You Have a Visitor',
                    name + ' is waiting for you at the Reception.',
                    'balaydalakay@gmail.com',
                    [staff_email, 'christopheranchetaece@gmail.com'],
                    fail_silently=True  # Changed to True to prevent errors from breaking the flow
                )
            except Exception as e:
                # Log the error but continue with the login process
                print(f"Email sending failed: {e}")
                
            return render(request, 'visitor/welcome.html', {'name': name})
    else:
        form = VisitorLoginForm()
    return render(request, 'visitor/login.html', {'form': form})

def welcome(request):
    return render(request, 'visitor/welcome.html')

def search_staff(request):
    """
    AJAX view to search for staff members based on a query string
    """
    from django.http import JsonResponse
    from .models import PersonToVisit
    
    query = request.GET.get('query', '')
    if query:
        staff_members = PersonToVisit.objects.filter(name__icontains=query).values('id', 'name')
        return JsonResponse(list(staff_members), safe=False)
    return JsonResponse([], safe=False)

def check_in(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.is_checked_in = True
            attendance.check_in_time = datetime.now()
            attendance.save()
            
            # Send notification to teacher
            try:
                teacher_email = attendance.child.teacher.email
                send_mail(
                    'Child Check-In',
                    f'{attendance.parent_name} has checked in {attendance.child.name} at {attendance.check_in_time}.',
                    'balaydalakay@gmail.com',
                    [teacher_email],
                    fail_silently=True
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Check-in successful!')
            return redirect('check_in')
    else:
        form = AttendanceForm()
    return render(request, 'visitor/check_in.html', {'form': form})

def check_out(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id, is_checked_in=True)
    
    if request.method == 'POST':
        attendance.is_checked_in = False
        attendance.is_checked_out = True
        attendance.check_out_time = datetime.now()
        attendance.save()
        
        # Send notification to teacher
        try:
            teacher_email = attendance.child.teacher.email
            send_mail(
                'Child Check-Out',
                f'{attendance.parent_name} has checked out {attendance.child.name} at {attendance.check_out_time}.',
                'balaydalakay@gmail.com',
                [teacher_email],
                fail_silently=True
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        messages.success(request, 'Check-out successful!')
        return redirect('check_out_list')
    
    return render(request, 'visitor/check_out.html', {'attendance': attendance})

def check_out_list(request):
    checked_in_attendances = Attendance.objects.filter(is_checked_in=True).order_by('-check_in_time')
    return render(request, 'visitor/check_out_list.html', {
        'attendances': checked_in_attendances
    })

def search_children(request):
    query = request.GET.get('query', '')
    if query:
        children = Child.objects.filter(name__icontains=query).values('id', 'name', 'class_name')
        return JsonResponse(list(children), safe=False)
    return JsonResponse([], safe=False)

def add_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Child added successfully!')
            return redirect('add_child')
    else:
        form = ChildForm()
    return render(request, 'visitor/add_child.html', {'form': form})

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully!')
            return redirect('add_teacher')
    else:
        form = TeacherForm()
    return render(request, 'visitor/add_teacher.html', {'form': form})

def search_staff(request):
    """
    AJAX view to search for staff members based on a query string
    """
    query = request.GET.get('query', '')
    if query:
        staff_members = Teacher.objects.filter(name__icontains=query).values('id', 'name')
        return JsonResponse(list(staff_members), safe=False)
    return JsonResponse([], safe=False)
