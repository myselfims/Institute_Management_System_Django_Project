
from django.contrib import admin

from home.models import *

# Register your models here.
# admin.site.register(Students)

@admin.register(StudentsDetails)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','gender','address']
    

    
@admin.register(StudentsAttendance)
class StudentsAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student_id','date']
    
@admin.register(StaffPermission)
class StaffPermissionAdmin(admin.ModelAdmin):
    list_display = ['username','permission']

@admin.register(Batches)
class BatchesAdmin(admin.ModelAdmin):
    list_display = ['subject','start_time', 'teacher','total_students']

@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ['permission_name']
    
@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ['course_name','pdf']
    
@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['username','subject','mobile',]
    
@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['subject']
    
@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student_id','course','start_date','status','end_date','marks']
    
admin.site.register(Schools)
admin.site.register(Addresses)
admin.site.register(Standard)
admin.site.register(RemovedAddmissions)