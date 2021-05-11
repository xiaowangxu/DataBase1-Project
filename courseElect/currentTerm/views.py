from django.shortcuts import render
from currentTerm.models import CurrentTerm
from course.models import Course
from django.http import JsonResponse
import json

# Create your views here.


def next_Term(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        term = CurrentTerm.objects.get(id=1)
        if (request.params['term'] == term.current):
            return JsonResponse({'state': 'failed', 'data': '已是当前学期'})
        try:
            target = Course.objects.get(term=request.params['term'])
        except Course.DoesNotExist:
            term.current = request.params['term']
            term.save()
            return JsonResponse({'state': 'ok', 'data': '进入下一学期！'})
        except:
            return JsonResponse({'state': 'failed', 'data': '学期重复'})
        else:
            return JsonResponse({'state': 'failed', 'data': '学期重复'})


def current_Term(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        term = CurrentTerm.objects.get(id=1)
        return JsonResponse({'state': 'ok', 'current': term.current})
