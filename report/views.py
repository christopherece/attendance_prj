from django.shortcuts import render
from visitor.models import Visitor
from django.db.models import Count
import json

def index(request):
    # Count visits for each person being visited
    visitor_query = Visitor.objects.values('person_to_visit__name') \
                                   .annotate(visit_count=Count('person_to_visit')) \
                                   .order_by('-visit_count')

    # Count visits for each date
    date_query = Visitor.objects.values('login_date') \
                                .annotate(visit_count=Count('login_date')) \
                                .order_by('login_date')

    # Prepare the data for the first chart (person visits)
    labels_visitors = [entry['person_to_visit__name'] for entry in visitor_query]
    data_visitors = [entry['visit_count'] for entry in visitor_query]

    # Prepare the data for the second chart (date visits)
    labels_dates = [entry['login_date'].strftime('%Y-%m-%d') for entry in date_query]
    data_dates = [entry['visit_count'] for entry in date_query]

    return render(request, 'report/index.html', {
        'labels_visitors': json.dumps(labels_visitors),
        'data_visitors': json.dumps(data_visitors),
        'labels_dates': json.dumps(labels_dates),
        'data_dates': json.dumps(data_dates),
    })
