from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from teacher.models import Teacher
from course.models import Course
from currentTerm.models import CurrentTerm
from django.core.paginator import Paginator
from django.db import connection
from django.db.utils import IntegrityError
from django.db.models.deletion import ProtectedError
import json

# Create your views here.


def get_Teacher(request):
    qs = Teacher.objects.values()
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            Teacher.objects.create(name=request.params['name'], tid=request.params['tid'],
                                   depart=request.params['depart'])
        except:
            return JsonResponse({'state': 'failed', 'data': '无法插入表项'})
        else:
            return JsonResponse({'state': 'ok', 'data': '已添加'})
    retStr = list(qs)
    return JsonResponse({'list': retStr})


def get_Teachers_Paged(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        qs = Teacher.objects.values()
        p = Paginator(qs, 10)
        pageidx = min(request.params["page"], p.num_pages)
        retStr = list(p.page(pageidx).object_list)
        return JsonResponse({'list': retStr, "pages": p.num_pages, "current": pageidx})


def login_Teacher(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Teacher.objects.get(tid=request.params['id'])
        except Teacher.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '教师不存在'})
        else:
            if target.password != request.params['password']:
                return JsonResponse({'state': 'failed', 'data': '密码错误'})
            else:
                return JsonResponse({'state': 'ok', 'id': target.id, 'tid': target.tid, 'name': target.name, 'isadmin': target.isadmin})


def reset_Teacher(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Teacher.objects.get(id=request.params['id'])
        except Teacher.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '教师不存在'})
        else:
            target.password = '1234567890'
            try:
                target.save()
            except:
                return JsonResponse({'state': 'failed', 'data': '无法修改'})
            else:
                return JsonResponse({'state': 'ok', 'data': '已重置密码为1234567890'})


def set_Teacher(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Teacher.objects.get(id=request.params['id'])
        except Teacher.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '教师不存在'})
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


def delete_Teacher(request):
    if (request.method == 'POST'):
        # print(request.body)
        request.params = json.loads(request.body)
        try:
            target = Teacher.objects.get(id=request.params['id'])
        except Teacher.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '教师不存在'})
        else:
            if target.isadmin:
                return JsonResponse({'state': 'failed', 'data': '无法删除管理员账号'})
            else:
                try:
                    target.delete()
                except ProtectedError:
                    return JsonResponse({'state': 'failed', 'data': '存在关联数据，无法删除'})
                else:
                    return JsonResponse({'state': 'ok', 'data': '已删除'})


def modify_Teacher(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Teacher.objects.get(id=request.params['id'])
        except Teacher.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '学生不存在'})
        else:
            target.name = request.params['name']
            target.tid = request.params['tid']
            target.depart = request.params['depart']
            try:
                target.save()
            except:
                return JsonResponse({'state': 'failed', 'data': '无法修改'})
            else:
                return JsonResponse({'state': 'ok', 'data': '修改完成'})


def get_Teacher_by_Depart(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        qs = Teacher.objects.values()
        qs = qs.filter(depart=request.params['depart'])
        retStr = list(qs)
        return JsonResponse({'list': retStr})


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_CourseGrade(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT e.id as euid , s.id as id, s.sid as sid, s.name as name, e.p_grade, e.e_grade, e.grade as grade, c.id as cuid FROM election_election e JOIN course_course c on E.cid_id = c.id join student_student s on e.sid_id = s.id WHERE c.id = %s", [request.params['id']])
            ret = list(dictfetchall(cursor))
            return JsonResponse({'list': ret})


def apply_Course(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            teacher = Teacher.objects.get(id=request.params['tid'])
            term = CurrentTerm.objects.get(id=1)
        except Teacher.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '教师不存在'})
        else:
            try:
                target = Course.objects.get(cid=request.params['cid'])
            except Course.DoesNotExist:
                try:
                    Course.objects.create(name=request.params['name'], cid=request.params['cid'], credit=request.params['credit'], capacity=request.params['capacity'], grade_percent=request.params['grade_percent'],
                                          term=term.current, description=request.params['description'], depart=teacher.depart, keys_tid=teacher)
                except:
                    return JsonResponse({'state': 'failed', 'data': '无法插入表项'})
                else:
                    return JsonResponse({'state': 'ok', 'data': '课程申请已提交'})
            else:
                return JsonResponse({'state': 'failed', 'data': '课号已存在'})


def get_ApplyCourse(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT C.id as id,C.cid as cid,C.name as name,C.credit as credit, C.capacity ,c.description as description, C.grade_percent, C.term as term,C.accept as accept from course_course C JOIN teacher_teacher T ON C.keys_tid_id = T.id WHERE T.id = %s and  C.term in (SELECT current FROM \"currentTerm_currentterm\" CT WHERE CT.id = 1)", [request.params['id']])
            ret = list(dictfetchall(cursor))
            return JsonResponse({'list': ret})


def delete_ApplyCourse(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Course.objects.get(id=request.params['id'])
        except Course.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '课程不存在'})
        else:
            try:
                target.delete()
            except:
                return JsonResponse({'state': 'failed', 'data': '课程无法删除'})
            else:
                return JsonResponse({'state': 'ok', 'data': '课程申请已删除'})


def get_CourseTerm(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT distinct C.term as term from course_course C JOIN teacher_teacher T ON C.keys_tid_id = T.id WHERE T.id = %s and C.accept ORDER BY term DESC", [request.params['id']])
            ret = list(dictfetchall(cursor))
            current = CurrentTerm.objects.get(id=1)
            return JsonResponse({'list': ret, 'current': current.current})
