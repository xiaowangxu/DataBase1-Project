from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from course.models import Course
from teacher.models import Teacher
from student.models import Student
from election.models import Election
import json

# Create your views here.


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_Course(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            t = Teacher.objects.get(id=request.params['tuid'])
            Course.objects.create(name=request.params['name'], cid=request.params['cid'],
                                  credit=request.params['credit'], depart=request.params['depart'], keys_tid=t)
        except:
            return JsonResponse({'state': 'failed', 'data': '无法插入表项'})
        else:
            return JsonResponse({'state': 'ok', 'data': '已添加'})
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT c.id id, c.name name, c.credit credit, c.cid cid, c.depart depart, t.name tname, t.id tuid, t.tid tid FROM course_course c JOIN teacher_teacher t on c.keys_tid_id = t.id")
        ret = list(dictfetchall(cursor))
        return JsonResponse({'list': ret})


def delete_Course(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Course.objects.get(id=request.params['id'])
        except Course.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '课程不存在'})
        else:
            target.delete()
            return JsonResponse({'state': 'ok', 'data': '已删除'})


def get_Course_by_Depart(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        qs = Course.objects.values()
        qs = qs.filter(depart=request.params['depart'])
        retStr = list(qs)
        return JsonResponse({'list': retStr})


def get_Course_by_Student(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            s = Student.objects.get(id=request.params['id'])
        except Student.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '学生不存在'})
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT C.id id, C.name name, C.cid cid, C.credit credit, C.depart depart, T.name tname, T.id tuid, T.tid tid FROM course_course C JOIN teacher_teacher T on C.keys_tid_id = T.id WHERE C.depart = %s", [s.depart])
                ret = list(dictfetchall(cursor))
                li = Election.objects.values()
                li = li.filter(sid=s.id, grade=None)
                return JsonResponse({'list': ret, 'elected': list(li)})


def get_Course_by_Teacher(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            t = Teacher.objects.get(id=request.params['id'])
        except:
            return JsonResponse({'state': 'failed', 'data': '教师不存在'})
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT C.id id, C.name name, C.credit credit, C.cid cid, C.depart depart, T.id tuid, T.tid tid, T.name tname FROM course_course C JOIN teacher_teacher T on T.id = C.keys_tid_id WHERE T.id = %s", [t.id])
                ret = list(dictfetchall(cursor))
                return JsonResponse({'list': ret})


def modify_Course(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Course.objects.get(id=request.params['id'])
        except Course.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '课程不存在'})
        else:
            try:
                t = Teacher.objects.get(id=request.params['tuid'])
            except:
                return JsonResponse({'state': 'failed', 'data': '无法修改'})
            else:
                target.name = request.params['name']
                target.cid = request.params['cid']
                target.keys_tid = t
                target.credit = request.params['credit']
                target.depart = request.params['depart']
                try:
                    target.save()
                except:
                    return JsonResponse({'state': 'failed', 'data': '无法修改'})
                else:
                    return JsonResponse({'state': 'ok', 'data': '修改完成'})
