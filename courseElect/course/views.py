from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from course.models import Course
from teacher.models import Teacher
from student.models import Student
from currentTerm.models import CurrentTerm
from election.models import Election
from django.db.models.deletion import ProtectedError
from django.core.paginator import Paginator
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
            term = CurrentTerm.objects.get(id=1)
            t = Teacher.objects.get(id=request.params['tuid'])
            Course.objects.create(name=request.params['name'], cid=request.params['cid'],
                                  credit=request.params['credit'], depart=request.params['depart'], description=request.params['description'], keys_tid=t, term=term.current, accept=True)
        except:
            return JsonResponse({'state': 'failed', 'data': '无法插入表项'})
        else:
            return JsonResponse({'state': 'ok', 'data': '已添加'})
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT c.id id, c.name name, c.description description, c.credit credit, c.cid cid, c.depart depart, t.name tname, t.id tuid, t.tid tid, c.term term FROM course_course c JOIN teacher_teacher t on c.keys_tid_id = t.id")
        ret = list(dictfetchall(cursor))
        return JsonResponse({'list': ret})


def get_Appliction_Paged(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT c.id id, c.name name, c.credit credit, c.description description, c.cid cid, c.depart depart, t.name tname, t.id tuid, t.tid tid, c.term term FROM course_course c JOIN teacher_teacher t on c.keys_tid_id = t.id WHERE C.accept is NULL ORDER BY term DESC, cid")
            qs = list(dictfetchall(cursor))
            p = Paginator(qs, 10)
            pageidx = min(request.params["page"], p.num_pages)
            retStr = list(p.page(pageidx).object_list)
            return JsonResponse({'list': retStr, "pages": p.num_pages, "current": pageidx})


def has_Appliction(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT count(C.id) count FROM course_course c JOIN teacher_teacher t on c.keys_tid_id = t.id WHERE C.accept is NULL ORDER BY term DESC, cid")
            qs = dictfetchall(cursor)[0]['count']
            return JsonResponse({'has': qs > 0})


def get_Course_Paged(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT c.id id, c.name name, c.description description, c.credit credit, c.cid cid, c.depart depart, t.name tname, t.id tuid, t.tid tid, c.term term FROM course_course c JOIN teacher_teacher t on c.keys_tid_id = t.id WHERE C.accept is TRUE ORDER BY term DESC, cid")
            qs = list(dictfetchall(cursor))
            p = Paginator(qs, 10)
            pageidx = min(request.params["page"], p.num_pages)
            retStr = list(p.page(pageidx).object_list)
            return JsonResponse({'list': retStr, "pages": p.num_pages, "current": pageidx})


def delete_Course(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Course.objects.get(id=request.params['id'])
        except Course.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '课程不存在'})
        else:
            try:
                target.delete()
            except ProtectedError:
                return JsonResponse({'state': 'failed', 'data': '存在关联数据，无法删除'})
            else:
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
            ret = []
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT C.id id, C.name name, C.cid cid, C.credit credit, C.description description, C.depart depart, T.name tname, T.id tuid, T.tid tid FROM course_course C JOIN teacher_teacher T on C.keys_tid_id = T.id WHERE C.depart = %s and C.id not in (SELECT cid_id FROM election_election WHERE sid_id = %s and grade is not NULL) and C.term in (SELECT current FROM currentTerm_currentterm) and C.accept is True", [s.depart, s.id])
                ret = list(dictfetchall(cursor))
            ret2 = []
            with connection.cursor() as cursor2:
                cursor2.execute(
                    "SELECT C.id cuid, cid, name, credit, depart, term, description FROM election_election E JOIN course_course C ON E.cid_id = C.id WHERE E.sid_id = %s and E.grade IS NULL and C.depart = %s and C.term in (SELECT current FROM currentTerm_currentterm)", [s.id, s.depart])
                ret2 = list(dictfetchall(cursor2))
                return JsonResponse({'list': ret, 'elected': ret2})


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
                    "SELECT C.id id, C.name name, C.credit credit, C.cid cid, C.depart depart, C.term term, T.id tuid, T.tid tid, T.name tname, A.avg FROM course_course C JOIN teacher_teacher T on T.id = C.keys_tid_id LEFT JOIN ( SELECT avg(grade) avg, cid_id cid FROM election_election GROUP BY cid_id ) A on A.cid = C.id WHERE T.id = %s and C.accept and C.term = %s", [t.id, request.params['term']])
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
                target.description = request.params['description']
                try:
                    target.save()
                except:
                    return JsonResponse({'state': 'failed', 'data': '无法修改'})
                else:
                    return JsonResponse({'state': 'ok', 'data': '修改完成'})


def modify_Application(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Course.objects.get(id=request.params['id'])
        except Teacher.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '课程不存在'})
        else:
            target.accept = request.params['accept']
            try:
                target.save()
            except:
                return JsonResponse({'state': 'failed', 'data': '无法修改'})
            else:
                return JsonResponse({'state': 'ok', 'data': '修改完成'})


def get_By_Course(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        print(request.params)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT S.sid sid, S.name name, E.grade grade, E.id eid, E.cid_id cid FROM election_election E JOIN student_student S ON S.id = E.sid_id WHERE cid_id = %s", [request.params['id']])
            ret = list(dictfetchall(cursor))
            return JsonResponse({'list': ret})


def delete_Election(request):
    if (request.method == 'POST'):
        request.params = json.loads(request.body)
        try:
            target = Election.objects.get(id=request.params['id'])
        except Election.DoesNotExist:
            return JsonResponse({'state': 'failed', 'data': '选课记录不存在'})
        else:
            try:
                target.delete()
            except ProtectedError:
                return JsonResponse({'state': 'failed', 'data': '存在关联数据，无法删除'})
            else:
                return JsonResponse({'state': 'ok', 'data': '已删除'})
