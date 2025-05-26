from django.shortcuts import render
from visitor.models import Attendance, Child, Teacher
from django.db.models import Count
import json

def index(request):
    # Count attendance for each child
    child_query = Attendance.objects.values('child__name', 'child__class_name') \
                                   .annotate(attendance_count=Count('child')) \
                                   .order_by('-attendance_count')

    # Count attendance for each date
    date_query = Attendance.objects.values('check_in_time__date') \
                                .annotate(attendance_count=Count('check_in_time__date')) \
                                .order_by('check_in_time__date')

    # Prepare the data for the first chart (child attendance)
    labels_children = []
    data_children = []
    for entry in child_query[:10]:  # Show top 10 most attended children
        labels_children.append(f"{entry['child__name']} ({entry['child__class_name']})")
        data_children.append(entry['attendance_count'])

    # Prepare the data for the second chart (daily attendance)
    labels_dates = [entry['check_in_time__date'].strftime('%Y-%m-%d') for entry in date_query]
    data_dates = [entry['attendance_count'] for entry in date_query]

    return render(request, 'report/index.html', {
        'labels_visitors': json.dumps(labels_visitors),
        'data_visitors': json.dumps(data_visitors),
        'labels_dates': json.dumps(labels_dates),
        'data_dates': json.dumps(data_dates),
    })
