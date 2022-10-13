from django.urls import path,include
from home import views


urlpatterns = [
    path('',views.landingpage),
    # path('login/', views.login),
    path('home/', views.home),
    path('staffauth/', views.staffauth),
    path('logout/', views.userlogout),
    path('dashboard/',views.dashboard),
    path('students/',views.students),
    path('students_attendance/',views.studentsattendace),
    path('attendance_save/',views.attendancesave),
    path('staff/',views.staff),
    path('editstaff/<str:username>',views.editstaff),
    path('savestaff/<str:username>',views.savestaff),
    path('addstaff/',views.addstaff),
    path('deletestaff/<str:username>',views.deletestaff),
    path('savenewstaff/',views.savenewstaff),
    path('studentsprogress/',views.students_progress),
    path('progress_save/<str:student_id>',views.porgres_save),
    path('addnewstudent/',views.addnewstudent),
    path('newstudentsave/',views.newstudentsave),
    path('studentupdatesave/',views.studentupdatesave),
    path('editstudent/<str:student_id>',views.editstudent),
    path('studentupdatesave/<str:student_id>',views.studentupdatesave),
    path('remove_admission/<str:student_id>',views.remove_admission),
    path('batches/',views.batches),
    path('addbatche/',views.addbatche),
    path('savebatche/',views.savebatche),
    path('editbatche/<str:id>',views.editbatche),
    path('search/',views.search),
    path('attendance_history/',views.attendance_history)
    # path('dashboard/',views.dashboard)
    # path('dashboard/',views.dashboard)
    # path('dashboard/',views.dashboard)
]
