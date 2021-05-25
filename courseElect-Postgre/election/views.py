from django.shortcuts import render
from student.models import Student
from course.models import Course
from election.models import Election
from django.http import JsonResponse
import json

# Create your views here.


def elect(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        ans = []
        try:
            s = Student.objects.get(id=request.params['id'])
        except Student.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '学生不存在'})
        else:
            # add
            for cuid in request.params['add']:
                try:
                    c = Course.objects.get(id=cuid)
                except Course.DoesNotExist:
                    ans.append(str(cuid) + ' 不存在')
                else:
                    Election.objects.create(sid=s, cid=c, grade=None)
            # remove
            for cuid in request.params['remove']:
                try:
                    c = Election.objects.get(sid=s, cid=cuid, grade=None)
                except Course.DoesNotExist:
                    ans.append(str(cuid) + ' 不存在')
                else:
                    c.delete()
            return JsonResponse({'state': 'ok', 'data': list(ans)})


def update(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        ans = []
        for item in request.params['list']:
            try:
                e = Election.objects.get(id=item['id'])
            except Election.DoesNotExist:
                ans.append('选课记录不存在')
            else:
                try:
                    e.grade = None
                    if (item['p_grade'] == ""):
                        e.p_grade = None
                    else:
                        e.p_grade = item['p_grade']
                    if (item['e_grade'] == ""):
                        e.e_grade = None
                    else:
                        e.e_grade = item['e_grade']
                    e.save()
                except Election.DoesNotExist:
                    ans.append('修改失败')
        return JsonResponse({'state': 'ok', 'data': list(ans)})
