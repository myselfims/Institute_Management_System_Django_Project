


from django.db import models

# Create your models here.

class StudentsDetails(models.Model):
    full_name = models.CharField(max_length=300,default="")
    photo = models.FileField(null=True,blank=True)
    mobile = models.CharField(max_length=10,default="")
    standard = models.CharField(max_length=50,default="")
    gender = models.CharField(max_length=300,default="")
    school = models.CharField(max_length=300,default="",null=True)
    address = models.CharField(max_length=300,default="",null=True)
    deposite = models.IntegerField(default=0,blank=True,null=True)
    dob = models.CharField(max_length = 100)
    admissiontime = models.DateTimeField(auto_now_add=True)
    computer_timing = models.CharField(max_length = 500,default="",blank=True,null=True)
    maktab_timing = models.CharField(max_length = 500,default="",blank=True,null=True)
    english_timing = models.CharField(max_length = 500,default="",blank=True,null=True)
    current_course = models.CharField(max_length=100, default="MS Paint", blank=True, null=True)
    start_date = models.CharField(max_length = 100,blank=True,null = True)

    def __str__(self) -> str:
        return self.full_name





class StudentsAttendance(models.Model):
    student_id = models.IntegerField()
    subject = models.CharField(max_length=100,default='')
    date = models.CharField(max_length=50,default='')
    status = models.CharField(max_length=20,default='')
    leavemsg = models.CharField(max_length=1000,default="",blank=True,null=True)
    
    def __str__(self) -> str:
        return str(self.student_id)

class StaffPermission(models.Model):
    username = models.CharField(max_length=200,default="")
    permission = models.CharField(max_length=100)

    


class Batches(models.Model):
    subject = models.CharField(max_length=200,default='',blank=True,null=True)
    teacher = models.CharField(max_length=200, default='',blank=True,null=True)
    start_time = models.CharField(max_length=100,default='',blank=True,null=True)
    end_time = models.CharField(max_length=100,default='',blank=True,null=True)
    max_capacity = models.CharField(max_length=100,default='',blank=True,null=True)
    min_capacity = models.CharField(max_length=100,default='',blank=True,null=True)
    total_students = models.CharField(max_length=100,default='0',blank=True,null=True)
    
class Permissions(models.Model):
    permission_name = models.CharField(max_length=200)
    
class Syllabus(models.Model):
    course_name = models.CharField(max_length=200,default="")
    pdf = models.FileField(null=True)
    
    def __str__(self) -> str:
        return self.course_name
    
    
class Subjects(models.Model):
    subject = models.CharField(max_length=200,default="")
    def __str__(self) -> str:
        return self.subject
    
class StaffMember(models.Model):
    username = models.CharField(max_length=200,default='')
    password = models.CharField(max_length=200,default='')
    subject = models.CharField(max_length=100,default='',blank=True, null = True)
    mobile = models.CharField(max_length=10,default='')
    
class StudentProgress(models.Model):
    student_id = models.IntegerField()
    course = models.CharField(max_length=300,default='')
    start_date = models.CharField(max_length=50,default='')
    status = models.CharField(max_length=50,default='in_progress')
    marks = models.CharField(max_length=20,default='',blank=True,null=True)
    end_date = models.CharField(max_length=50,default='',blank=True,null=True)
    
class Schools(models.Model):
    school_name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.school_name
    
class Addresses(models.Model):
    address = models.CharField(max_length = 200)
    def __str__(self) -> str:
        return self.address
    
class Standard(models.Model):
    standard = models.CharField(max_length=100)
    
class RemovedAddmissions(models.Model):
    student_id = models.IntegerField()
    reason = models.CharField(max_length = 5000)
    date = models.DateField(auto_now_add = True)