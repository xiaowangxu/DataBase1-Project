from django.shortcuts import render
from currentTerm.models import CurrentTerm
from course.models import Course
from django.http import JsonResponse
from django.db import connection
import json

# Create your views here.


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def next_Term(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT new_term(%s)", [request.params['term']])
            ret = list(dictfetchall(cursor))[0]
            if (ret['new_term'] == 'success'):
                return JsonResponse({'state': 'ok', 'data': '进入下一学期了！！！'})
            else:
                return JsonResponse({'state': 'failed', 'data': ret['new_term']})


def current_Term(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        term = CurrentTerm.objects.get(id=1)
        return JsonResponse({'state': 'ok', 'current': term.current})
