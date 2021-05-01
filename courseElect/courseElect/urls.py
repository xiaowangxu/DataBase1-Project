"""courseElect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from student.views import get_Students, delete_Students, modify_Student, login_Student, reset_Student, set_Student
import student.views
from teacher.views import get_Teacher, reset_Teacher, login_Teacher, delete_Teacher, modify_Teacher, get_Teacher_by_Depart, set_Teacher, get_CourseGrade, apply_Course, get_ApplyCourse, delete_ApplyCourse, get_CourseTerm
from course.views import get_Course, delete_Course, get_Course_by_Depart, get_Course_by_Student, modify_Course, get_Course_by_Teacher, get_By_Course, delete_Election
from election.views import elect, update

urlpatterns = [
    path('admin/', admin.site.urls),

    # Student
    path('students/', get_Students),
    path('students/delete/', delete_Students),
    path('students/login/', login_Student),
    path('students/modify/', modify_Student),
    path('students/resetPassword/', reset_Student),
    path('students/setPassword/', set_Student),
    path('students/getCourse/', student.views.get_Course),
    path('students/getByCourse/', get_By_Course),
    path('students/getCourseTerm/', student.views.get_CourseTerm),
    path('students/getGPAs/', student.views.get_GPAs),

    # Teacher
    path('teacher/', get_Teacher),
    path('teacher/delete/', delete_Teacher),
    path('teacher/login/', login_Teacher),
    path('teacher/modify/', modify_Teacher),
    path('teacher/getDepart/', get_Teacher_by_Depart),
    path('teacher/getCourse/', get_Course_by_Teacher),
    path('teacher/getCourseGrade/', get_CourseGrade),
    path('teacher/setPassword/', set_Teacher),
    path('teacher/resetPassword/', reset_Teacher),
    path('teacher/updateGrade/', update),
    path('teacher/applyCourse/', apply_Course),
    path('teacher/getApplyCourse/', get_ApplyCourse),
    path('teacher/deletApplyCourse/', delete_ApplyCourse),
    path('teacher/getCourseTerm/', get_CourseTerm),

    # Course
    path('course/', get_Course),
    path('course/delete/', delete_Course),
    path('course/modify/', modify_Course),
    path('course/getDepart/', get_Course_by_Depart),
    path('course/getStudent/', get_Course_by_Student),
    path('course/elect/', elect),
    path('course/deleteElect/', delete_Election)
]
