
from ast import Sub
from email import message
from itertools import count
from webbrowser import BackgroundBrowser
from django.shortcuts import render,HttpResponse
from .models import Addresses, Batches, Permissions, RemovedAddmissions, Schools, StaffMember, Standard, StudentProgress, StudentsDetails, StaffPermission, Subjects,Syllabus,StudentsAttendance
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.contrib import messages
from django.template.defaulttags import register
from datetime import date
from django.views.decorators.csrf import csrf_exempt


# Create your views here.




def landingpage(request):
    if request.user.is_authenticated:
        return redirect('home/')
    return render(request,'landing.html')

def userlogout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def staffauth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(str(user)+'user')
        if user is not None:
            login(request,user)
            return redirect('/home/')
        else:
            messages.error(request,'Invalid Credential!')
            return redirect('/')
            

def dashboard(request):
    if request.user.is_authenticated:
        return render(request,'dashboard.html')
    return redirect('/')
def home(request):
    if request.user.is_authenticated:
        superuser = 'no'
        print('yaha tak ara')
        if request.user.is_superuser:
            superuser = 'yes'
            perm = StaffPermission.objects.filter(username=request.user.username)
            if len(perm) == 0:
                createperm = StaffPermission.objects.create(username=request.user.username,permission = 'Superuser')
                createperm.save()
                
        userpermissions = StaffPermission.objects.filter(username=request.user.username)
        students = StudentsDetails.objects.all()
        syllabus = Syllabus.objects.all()
        counter = {
            
        }
        for course in syllabus:
            total = StudentsDetails.objects.filter(current_course=course)
            counter[str(course)]= len(total)
        print('yaha tak ara')
        return render(request,'home.html',{'students':students,'staffpermissions':userpermissions,'syllabus':syllabus,'enrolled':counter,'user':request.user.username,})
    return redirect('/')
    
@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)   

def students(request):
    if request.user.is_authenticated:
        superuser = 'no'
        if request.user.is_superuser:
            superuser = 'yes'
            perm = StaffPermission.objects.filter(username=request.user.username,permission = 'Superuser')
            if len(perm) == 0:
                createperm = StaffPermission.objects.create(username=request.user.username,permission = 'Superuser')
                createperm.save()
        removed_admissions = []
        admissions = RemovedAddmissions.objects.all()
        for admission in admissions:
            removed_admissions.append(int(admission.student_id))
        print(removed_admissions)
        students = StudentsDetails.objects.all()
        userpermissions = StaffPermission.objects.filter(username=request.user.username)
        return render(request,'students.html',{'students':students,'staffpermissions':userpermissions,'removedadmissions':removed_admissions})
    return redirect('/')

def studentsattendace(request):
    if request.user.is_authenticated:
        todaysdate = date.today()
        print(todaysdate)
        students = StudentsDetails.objects.all()
        batch = Batches.objects.filter(subject='computer')
        alreadyattendentcomputer = []
        alreadyattendentmaktab = []
        alreadyattendentenglish = []
        userpermissions = StaffPermission.objects.filter(username=request.user.username)
        if request.user.is_superuser:
            for student in students:
                attendance = StudentsAttendance.objects.filter(student_id= student.id, subject = 'Computer_Attendance',date=todaysdate)
                for id in attendance:
                    alreadyattendentcomputer.append(int(id.student_id))
            perm = StaffPermission.objects.filter(username=request.user.username)
            if len(perm) == 0:
                createperm = StaffPermission.objects.create(username=request.user.username,permission = 'superuser')
                createperm.save()
            
        else:
            for student in students:
                for permission in userpermissions:
                    attendance = StudentsAttendance.objects.filter(student_id= student.id, subject = permission.permission,date=todaysdate)
                    for id in attendance:
                        alreadyattendentcomputer.append(int(id.student_id))
        print(alreadyattendentcomputer)
        attendance = StudentsAttendance.objects.all()
        batches = Batches.objects.filter(teacher = request.user.username)
        if request.method == 'GET':
            query = request.GET.get('query')
            for s in students:
                if str(query).lower() in str(s.full_name).lower() or str(query) in str(student.id) or str(query).lower() in str(s.current_course).lower() or str(query).lower() in str(s.mobile).lower():
                    students = StudentsDetails.objects.filter(full_name=s.full_name,id = s.id)
            return render(request,'attendance.html',{'students':students,'staffpermissions':userpermissions,'savedcomputerattendance':alreadyattendentcomputer,'date':todaysdate,'batches':batch,'studentattendance':attendance,'batches':batches,'query':query})
            
        return render(request,'attendance.html',{'students':students,'staffpermissions':userpermissions,'savedcomputerattendance':alreadyattendentcomputer,'date':todaysdate,'batches':batch,'studentattendance':attendance,'batches':batches})
        
    else:
        return redirect('/')
    
    
def attendancesave(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            student_id = request.POST.get('student_id')
            subject = request.POST.get('subject')
            status = request.POST.get('status'+student_id)
            leavemsg = request.POST.get('leavemsg')
            print(student_id)
            print(subject)
            print(date.today())
            print(status)
            attendance = StudentsAttendance.objects.create(student_id=student_id,subject=subject,date=date.today(),status=status,leavemsg=leavemsg)
            attendance.save()
            return redirect('/students_attendance/')
    return redirect('/')   
def staff(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        userpermissions = StaffPermission.objects.filter(username=request.user.username)
        syllabus = Syllabus.objects.all()
        subjects = Subjects.objects.all()
        staffmembers = StaffMember.objects.all()
        return render(request,'staff.html',{'subjects':subjects,'staffpermissions':userpermissions,'members':staffmembers})
    else:
        return redirect('/')
    
def editstaff(request,username):
    if request.user.is_authenticated:
        staffmember = StaffMember.objects.get(username=username)
        print(staffmember)
        userpermissions = StaffPermission.objects.filter(username=request.user.username)
        editmemberpermissions = StaffPermission.objects.filter(username=username)
        permissions = Permissions.objects.all()
        for perm in editmemberpermissions: 
            if perm.permission == 'Superuser':
                permissions = Permissions.objects.filter(permission_name = perm.permission)
        print(userpermissions)
        subjects = Subjects.objects.all()
        batches = Batches.objects.all()
        return render(request,'staffform.html',{'subjects':subjects,'staffpermissions':userpermissions,'member':staffmember,'batches':batches,'permissions':permissions,'editmemberpermissions':editmemberpermissions})
    return redirect('/')

def savestaff(request,username):
    if request.user.is_authenticated:
        newusername = request.POST.get('username')
        password = request.POST.get('password')
        subject = request.POST.get('subject')
        contact = request.POST.get('contact')
        allperm = Permissions.objects.all()
        for perm in allperm:
            permitted = request.POST.get('permitted'+perm.permission_name)
            permitted = str(permitted)
            if len(permitted) > 4 and 'delete' in permitted:
                delperm = StaffPermission.objects.get(username=username,permission=perm.permission_name)
                delperm.delete()
                if 'deleteSuperuser' in permitted:
                    print('yaha ara')
                    user = User.objects.get(username=username)
                    user.is_admin = False
                    user.is_staff = False
                    user.save()
            print(permitted)
        permission = request.POST.get('permission')
        print(permission)
        perm = StaffPermission.objects.filter(username=username,permission = 'Superuser')
        print(len(perm))
        permission = str(permission)
        if len(perm) == 0 and 'Superuser' in permission:
            user = User.objects.get(username = username)
            user.is_admin = True
            user.is_staff = True
            user.save()
            previousperm = StaffPermission.objects.filter(username=username)
            if len(previousperm) > 0 or previousperm is not None:
                for perm in previousperm:
                    perm.delete()
            
            createperm = StaffPermission.objects.create(username=newusername,permission = 'Superuser')
            createperm.save()
            return redirect('/staff/')
        else:
            permission = str(permission)
            print(permission)
            staffpermcheck = StaffPermission.objects.filter(username=newusername,permission=permission)
            alreadypermitted = StaffPermission.objects.filter(username=newusername)
            if 'Maktab_Attendance' in permission or 'Computer_Attendance' in permission or 'English_Attendance' in permission:
                for perm in alreadypermitted: 
                    if perm.permission == 'Computer_Attendance':
                        messages.error(request,'You have already Computer Attendance')
                        return redirect('/editstaff/'+newusername)
                    elif perm.permission == 'English_Attendance':
                        messages.error(request,'You have already English Attendance')
                        return redirect('/editstaff/'+newusername)
                    elif perm.permission == 'Maktab_Attendance':
                        messages.error(request,'You have already Computer Attendance')
                        return redirect('/editstaff/'+newusername)
            print(len(staffpermcheck))
            if len(staffpermcheck) == 0 or staffpermcheck is None and len(permission) > 4:
                staffperm = StaffPermission.objects.create(username=newusername,permission=permission)
                staffperm.save()
            user = User.objects.get(username = username)
            user.username = newusername
            user.set_password(password)
            user.save()
            staff = StaffMember.objects.get(username = username)
            staff.username = newusername
            staff.password = password
            print(subject)
            staff.subject = subject
            
            staff.mobile = contact
            
            staff.save()
        return redirect('/editstaff/'+newusername)
    return redirect('/')
    
def deletestaff(request,username):
    if request.method == 'POST':
        formusername = request.POST.get('username')
        if formusername == username:
            user = User.objects.get(username=username)
            user.delete()
            staffmember = StaffMember.objects.get(username = username)
            staffmember.delete()
            perms = StaffPermission.objects.filter(username=username)
            for perm in perms:
                perm.delete()
            return redirect('/staff/')
        messages.error(request,'Entered wrong username !')
        return redirect('/editstaff/'+username)
        
    
    
    
    
    
    
def students_progress(request):
        if request.user.is_authenticated:
  
            if request.user.is_superuser:
                perm = StaffPermission.objects.filter(username=request.user.username,permission = 'Superuser')
                if len(perm) == 0:
                    createperm = StaffPermission.objects.create(username=request.user.username,permission = 'Superuser')
                    createperm.save()
            current_course = StudentProgress.objects.all()
            students = StudentsDetails.objects.all()
            removed_admissions = []
            admissions = RemovedAddmissions.objects.all()
            for admission in admissions:
                removed_admissions.append(int(admission.student_id))
            print(removed_admissions)
            userpermissions = StaffPermission.objects.filter(username=request.user.username)
            return render(request,'progress.html',{'students':students,'staffpermissions':userpermissions,'currentcourse':current_course,'removedadmissions':removed_admissions})
        return redirect('/')
    
    
def porgres_save(request, student_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            marks = request.POST.get('marks')
            student = StudentsDetails.objects.get(id = student_id)
            courses = Syllabus.objects.all()
            todaydate = date.today()
            progress_save = StudentProgress.objects.create(student_id = student_id,course= student.current_course,start_date = student.start_date,marks= marks,end_date= todaydate)
            progress_save.save()
            next_course = ''
            for course in courses:
                if len(next_course) > 0:
                    student.current_course = course.course_name
                    student.start_date = todaydate
                    student.save()
                    break
                if student.current_course == course.course_name:
                    next_course = course.course_name
            messages.success(request,'Successfully updated!')
            return redirect('/studentsprogress/')

    
    
def addstaff(request):
    if request.user.is_authenticated and request.user.is_superuser:
        syllabus = Syllabus.objects.all()
        subjects = Subjects.objects.all()
        staffmembers = StaffMember.objects.all()
        batches = Batches.objects.all()
        permissions = Permissions.objects.all()
        return render(request,'addstaffform.html',{'subjects':subjects,'batches':batches,'permissions':permissions})
    return HttpResponse('your not superuser')

def savenewstaff(request):
     if request.user.is_authenticated:
        username = request.POST.get('username')
        password = request.POST.get('password')
        subject = request.POST.get('subject')
        contact = request.POST.get('contact')
        permission = request.POST.get('permission')
        
        user = User.objects.filter(username=username)
        if len(user) == 0 or user == None:
            createuser = User.objects.create(username=username,password=password)
            createuser.set_password(password)
            createuser.save()
            
            if permission == 'Superuser':
                user = User.objects.get(username=username)
                user.is_admin = True
                user.is_staff = True
                user.save()
            createstaff = StaffMember.objects.create(username = username, password= password,subject = subject,mobile=contact)
            createstaff.save()
            if permission is not None:
                createperm = StaffPermission.objects.create(username=username,permission=permission)
                createperm.save()
            return redirect('/staff/')
        messages.error(request,'Username already exist !')
        return redirect('/addstaff/')
     return redirect('/')

def addnewstudent(request):
    schools = Schools.objects.all()
    addresses = Addresses.objects.all()
    standards = Standard.objects.all()
    batches = Batches.objects.all()
    return render(request,'addnewstudent.html',{'schools':schools,'addresses':addresses,'standards':standards,'batches':batches})


def newstudentsave(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        picture = request.POST.get('picture')
        gender = request.POST.get('gender')
        standard = request.POST.get('standard')
        school = request.POST.get('school')
        address = request.POST.get('address')
        deposite = request.POST.get('deposite')
        dob = request.POST.get('dob')
        computer_timing = request.POST.get('computer_timing')
        english_timing = request.POST.get('english_timing')
        maktab_timing = request.POST.get('maktab_timing')
        todaydate = date.today()
        if len(computer_timing) > 4 :
            computer_batch = Batches.objects.get(subject='Computer',start_time = computer_timing)
            computer_batch.total_students = int(computer_batch.total_students) + 1
            computer_batch.save()
        elif len(english_timing) > 4 :
            computer_batch = Batches.objects.get(subject='English',start_time = computer_timing)
            computer_batch.total_students = int(computer_batch.total_students) + 1
            computer_batch.save()
        elif len(maktab_timing) > 4 :
            computer_batch = Batches.objects.get(subject='Arabic',start_time = computer_timing)
            computer_batch.total_students = int(computer_batch.total_students) + 1
            computer_batch.save()
        
        student = StudentsDetails.objects.create(full_name=name,photo=picture, mobile=mobile, standard=standard, gender=gender, school=school, address=address, deposite=deposite, dob=dob, computer_timing=computer_timing, maktab_timing= maktab_timing, english_timing=english_timing, start_date=todaydate )
        student.save()
        messages.success(request,'Successfully saved !')
        return redirect('/addnewstudent/')
    return redirect('/addnewstudent/')


def editstudent(request,student_id):
    if request.user.is_authenticated:
        student = StudentsDetails.objects.get(id=student_id)
        schools = Schools.objects.all()
        addresses = Addresses.objects.all()
        standards = Standard.objects.all()
        batches = Batches.objects.all()
        subjects = Subjects.objects.all()
        teachers = StaffMember.objects.all()
        return render(request,'studenteditform.html',{'student':student,'schools':schools,'addresses':addresses,'standards':standards,'subjects':subjects,'teachers':teachers,'batches':batches})
    return redirect('/')

def studentupdatesave(request, student_id):
    if request.user.is_superuser:
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        picture = request.POST.get('picture')
        gender = request.POST.get('gender')
        standard = request.POST.get('standard')
        school = request.POST.get('school')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        computer_timing = request.POST.get('computer_timing')
        english_timing = request.POST.get('english_timing')
        maktab_timing = request.POST.get('maktab_timing')
        student = StudentsDetails.objects.get(id=student_id)
     
        if len(str(computer_timing)) > 4 :
            if str(computer_timing) != str(student.computer_timing):
                print('here')
                try:
                    oldbatch = Batches.objects.get(subject = 'Computer',start_time = student.computer_timing)
                    print(oldbatch)
                    oldbatch.total_students = int(oldbatch.total_students) - 1
                    oldbatch.save()
                except:
                    pass

            computer_batch = Batches.objects.get(subject='Computer',start_time = computer_timing)
            computer_batch.total_students = int(computer_batch.total_students) + 1
            computer_batch.save()
        elif len(str(english_timing)) > 4 :
            if english_timing != student.english_timing:
                try:
                    oldbatch = Batches.objects.get(subject = 'English',start_time= student.english_timing)
                   
                    oldbatch.total_students = int(oldbatch.total_students) - 1
                    oldbatch.save()
                except:
                    pass
            computer_batch = Batches.objects.get(subject='English',start_time = computer_timing)
            computer_batch.total_students = int(computer_batch.total_students) + 1
            computer_batch.save()
        elif len(str(maktab_timing)) > 4 :
            if maktab_timing != student.maktab_timing:
                try:
                    oldbatch = Batches.objects.get(subject = 'Arabic',start_time= student.maktab_timing)
               
                    oldbatch.total_students = int(oldbatch.total_students) - 1
                    oldbatch.save()
                except:
                    pass
            computer_batch = Batches.objects.get(subject='Arabic',start_time = computer_timing)
            computer_batch.total_students = int(computer_batch.total_students) + 1
            
            computer_batch.save()
            
        student.full_name = name
        student.mobile = mobile
        student.photo = picture
        student.gender = gender
        student.standard = standard
        student.school = school
        student.address = address
        student.dob = dob
        student.computer_timing = computer_timing
        student.english_timing = english_timing
        student.maktab_timing = maktab_timing
        
        
        student.save()
        messages.success(request,'Successfully updated !')
        return redirect('/editstudent/'+student_id)
        student = StudentsDetails.objects.get(student_id=student_id)
    return HttpResponse('Your not superuser please go back to homepage!')


def batches(request):
    if request.user.is_superuser:
        students = StudentsDetails.objects.all()
        userpermissions = StaffPermission.objects.filter(username=request.user.username)
        batches = Batches.objects.all()
        return render(request,'batches.html',{'students':students,'staffpermissions':userpermissions,'batches':batches})
    return redirect('/home/')


def addbatche(request):
    if request.user.is_superuser:
        students = StudentsDetails.objects.all()
        userpermissions = StaffPermission.objects.filter(username=request.user.username)
        batches = Batches.objects.all()
        subjects = Subjects.objects.all()
        teachers = StaffMember.objects.all()
        return render(request,'addbatch.html',{'students':students,'staffpermissions':userpermissions,'batches':batches,'subjects':subjects,'teachers':teachers})
    
def savebatche(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            subject = request.POST.get('subject')
            teacher = request.POST.get('teacher')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            max_capacity = request.POST.get('max_capacity')
            min_capacity = request.POST.get('min_capacity')
            
            batchcheck = Batches.objects.filter(subject=subject,teacher=teacher,start_time=start_time)
            if len(batchcheck) == 0:
                batche = Batches.objects.create(subject=subject,teacher=teacher,start_time=start_time,end_time=end_time,max_capacity=max_capacity,min_capacity=min_capacity)
                batche.save()
            else:
                messages.error(request,'Batche already exist !')
                return redirect('/addbatche/')

            messages.success(request,'Batche successfully created ! ')
            return redirect('/addbatche/')
    

def search(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            query = request.GET.get('query')
            students = StudentsDetails.objects.all()
            
            searched = []
            for student in students:
                print(str(student.full_name))
                print(str(query))
                if str(query).lower() in str(student.full_name).lower() or str(query) in str(student.id) or str(query).lower() in str(student.current_course).lower() or str(query).lower() in str(student.mobile).lower():
                    searched.append(student.id)
                print(searched)
            userpermissions = StaffPermission.objects.filter(username=request.user.username)
            return render(request,'studentssearch.html',{'students':students,'staffpermissions':userpermissions,'searched': searched})
    return redirect('/')

   
def editbatche(request,id):
    if request.user.is_superuser:
        batch = Batches.objects.get(id=id)
        students = StudentsDetails.objects.all()
        userpermissions = StaffPermission.objects.filter(username=request.user.username)
        batches = Batches.objects.all()
        subjects = Subjects.objects.all()
        teachers = StaffMember.objects.all()
        return render(request,'editbatch.html',{'students':students,'staffpermissions':userpermissions,'batches':batches,'subjects':subjects,'teachers':teachers,'batch':batch})
        
        
    return redirect('/home/')

def attendance_history(request):
    if request.user.is_authenticated:
        superuser = 'no'
        if request.user.is_superuser:
            superuser = 'yes'
            perm = StaffPermission.objects.filter(username=request.user.username,permission = 'Superuser')
            if len(perm) == 0:
                createperm = StaffPermission.objects.create(username=request.user.username,permission = 'Superuser')
                createperm.save()
    
            students = StudentsDetails.objects.all()
            userpermissions = StaffPermission.objects.filter(username=request.user.username)
            attendance = StudentsAttendance.objects.all()
            models = []
            todaysdate = date.today()
            for attend in attendance:
                if str(todaysdate.month) in str(attend.date[:7]):
                    models.append(attend)
            attend = []
            for a in attendance:
                print(a.student_id)
            return render(request,'attendance_history.html',{'students':students,'staffpermissions':userpermissions,'allattendance':models,'attend':attend})
    return redirect('/')

def remove_admission(request, student_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            reason = request.POST.get('reason')
            remove = RemovedAddmissions.objects.create(student_id=student_id,reason = reason)
            remove.save()
            messages.success(request,'Admission removed!')
            return redirect('/students/')





























