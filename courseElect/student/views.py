from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from student.models import Student
from currentTerm.models import CurrentTerm
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.db.models.deletion import ProtectedError
from django.db import connection
import json
from django.core.paginator import Paginator

# Create your views here.


def get_Students(request):
    qs = Student.objects.values()
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            Student.objects.create(name=request.params['name'], sid=request.params['sid'],
                                   sex=request.params['sex'], birth=request.params['birth'], depart=request.params['depart'])
        except:
            return JsonResponse({'state': 'failed', 'data': '无法插入表项'})
        else:
            return JsonResponse({'state': 'ok', 'data': '已添加'})
    retStr = list(qs)
    return JsonResponse({'list': retStr})


def get_Students_Paged(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        qs = Student.objects.values()
        p = Paginator(qs, 10)
        pageidx = min(request.params["page"], p.num_pages)
        retStr = list(p.page(pageidx).object_list)
        return JsonResponse({'list': retStr, "pages": p.num_pages, "current": pageidx})


def login_Student(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Student.objects.get(sid=request.params['id'])
        except Student.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '学生不存在'})
        else:
            if target.password != request.params['password']:
                return JsonResponse({'state': 'failed', 'data': '密码错误'})
            else:
                return JsonResponse({'state': 'ok', 'id': target.id, 'sid': target.sid, 'name': target.name})


def delete_Students(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Student.objects.get(id=request.params['id'])
        except Student.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '学生不存在'})
        else:
            try:
                target.delete()
            except ProtectedError:
                return JsonResponse({'state': 'failed', 'data': '存在关联数据，无法删除'})
            else:
                return JsonResponse({'state': 'ok', 'data': '已删除'})


def modify_Student(request):
    if (request.method == 'POST'):
        print(request.body)
        request.params = json.loads(request.body)
        try:
            target = Student.objects.get(id=request.params['id'])
        except Student.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '学生不存在'})
        else:
            target.name = request.params['name']
            target.sex = request.params['sex']
            target.birth = request.params['birth']
            target.sid = request.params['sid']
            target.depart = request.params['depart']
            try:
                target.save()
            except:
                return JsonResponse({'state': 'failed', 'data': '无法修改'})
            else:
                return JsonResponse({'state': 'ok', 'data': '修改完成'})


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_Course(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT C.id, C.cid, C.name cname, C.depart, C.credit, E.grade, T.id tuid, T.tid, T.name tname, C.term term FROM election_election E JOIN student_student S on E.sid_id = S.id JOIN course_course C on C.id = E.cid_id JOIN teacher_teacher T on T.id = C.keys_tid_id WHERE S.id = %s and C.term = %s", [request.params['id'], request.params['term']])
            ret = list(dictfetchall(cursor))
            return JsonResponse({'list': ret})


def reset_Student(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Student.objects.get(id=request.params['id'])
        except Student.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '学生不存在'})
        else:
            target.password = '1234567890'
            try:
                target.save()
            except:
                return JsonResponse({'state': 'failed', 'data': '无法修改'})
            else:
                return JsonResponse({'state': 'ok', 'data': '已重置密码为1234567890'})


def set_Student(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Student.objects.get(id=request.params['id'])
        except Student.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '学生不存在'})
        else:
            if target.password != request.params['old']:
                return JsonResponse({'state': 'failed', 'data': '旧密码错误'})
            target.password = request.params['new']
            try:
                target.save()
            except:
                return JsonResponse({'state': 'failed', 'data': '无法修改'})
            else:
                return JsonResponse({'state': 'ok', 'data': '已修改密码'})


def get_CourseTerm(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute("SELECT distinct C.term term from course_course C JOIN election_election E ON E.cid_id=C.id WHERE E.sid_id= %s ORDER BY term DESC", [
                           request.params['id']])
            ret = list(dictfetchall(cursor))
            current = CurrentTerm.objects.get(id=1)
            return JsonResponse({'list': ret, 'current': current.current})


def get_GPAs(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT term term, avg(grade) avg, sum(jd * credit)/sum(credit) gpa FROM (SELECT C.term, E.grade, (CASE WHEN grade >= 90 THEN 4.0 WHEN grade >=85 THEN 3.7 WHEN grade >=83 THEN 3.3 WHEN grade >=78 THEN 3.0 WHEN grade >=75 THEN 2.7 WHEN grade >=72 THEN 2.3 WHEN grade >=68 THEN 2.0 WHEN grade >=64 THEN 1.7 WHEN grade >=60 THEN 1.0 ELSE 0.0 END ) as jd, C.credit FROM election_election E JOIN course_course C on E.cid_id = C.id WHERE E.sid_id = %s and C.term not in (SELECT current from currentTerm_currentterm)) GROUP BY term ORDER BY term DESC", [request.params['id']])
            ret = list(dictfetchall(cursor))
            return JsonResponse({'list': ret})
