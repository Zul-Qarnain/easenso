from django.db import connection
from django.http          import HttpResponseRedirect, HttpResponse
from django.shortcuts     import render, render_to_response, RequestContext
from django.contrib.auth import authenticate, login
from pis_objects.student  import *
from pis_objects.employee import *
from pis_system.models    import *
from pis_system.forms     import ItemSearch, LogInForm
from .forms               import *
from helpers.helpers      import *
import datetime

SYSTEM_NAME = "Registration Module"


def registration(request):
    context = RequestContext(request)
    user = request.session.get('user')
    data = {'system_name': SYSTEM_NAME,
            'page' : 'view_student',
            'action_url' : ''
    }

    if user is not None: #and hasValidUserGrpAccess(user['id'], 'student'):
        return HttpResponseRedirect('/registration/searchRegStud')
    elif request.method == 'POST': # authenticate user
        login_form = LogInForm(request.POST)
        if login_form.is_valid():
            employee = authenticate(username=login_form.cleaned_data['userID'], password=login_form.cleaned_data['password'])
            if employee is not None and employee.is_active and hasAccess(employee.id, 'student'):
                login(request, employee)
                request.session['user'] = {'id':employee.id, 'userID': employee.username, 'firstname':employee.first_name, 'lastname':employee.last_name}
                return HttpResponseRedirect('/registration/searchRegStud')
            else:
                data['form'] = login_form
                return render_to_response('login.html', data, context)
        else:
            data['errors'] = login_form.errors
            data['form'] = login_form
            return render_to_response('login.html', data, context)
    else:#login precedes
        data['form'] = LogInForm()
        return render_to_response('login.html', data, context)
        
    
def searchRegStudents(request):
    context  = RequestContext(request)
    data = {
        'system_name' : SYSTEM_NAME,
        'page' : 'view_student',
    }

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_key = search_form.cleaned_data['options']
            search_val = search_form.cleaned_data['search']
            if search_key == 'studentID':
                students = Student.objects.filter(studentID__contains=search_val)
            elif search_key == 'firstname':
                students = Student.objects.filter(firstname__contains=search_val)
            elif search_key == 'lastname':
                students = Student.objects.filter(lastname__contains=search_val)

            data['students'] = students
            data['search_form'] = search_form
            return render_to_response('./registration/searchview_stud.html', data, context)
        else:
           data['search_form'] = search_form
           return render_to_response('./registration/searchview_stud.html', data, context) 
            
    else: # display only the form
        data['search_form'] = SearchForm()
        return render_to_response('./registration/searchview_stud.html', data, context)


#this function renders login form   
def reg_login(request):
    form       = LogInForm()
    page       = 'login.html'
    sys_name   = 'Student Registration'
    cover_url  = '/static/images/billing_cover.jpg'
    action_url = 'validate_user'
    feedback   = 'Sample Feedback'
    return render(request, 
           page, 
           {  'form'        : form, 
              'system_name' : sys_name, 
              'cover_url'   : cover_url, 
              'action_url'  : action_url, 
              'feedback'    : feedback
           }
    )


def genStudentID(request):
    id = '%s' %genStudId()
    while Student.objects.filter(studentID=id).exists():
        id = '%s' %genStudId()
        
    return HttpResponse(id)


#regStud function registers new student and corresponding bills for new student
def regStud(request): #add and edit student information
    context = RequestContext(request)
    data = {
        'action'      : request.GET.get('action', 'add'),
        'system_name' : SYSTEM_NAME
    }
    sat  = "/registration/regStud/"
    
    if request.method == 'POST':
        stud_form = StudentForm(request.POST, request.FILES)
        if stud_form.is_valid():
            if request.POST["action"] == 'add':
                student = Student(
                    studentID               = stud_form.cleaned_data['studentID'], 
                    firstname               = stud_form.cleaned_data['firstname'],
                    mi                      = stud_form.cleaned_data['mi'],
                    lastname                = stud_form.cleaned_data['lastname'],
                    gender                  = stud_form.cleaned_data['gender'],
                    date_of_birth           = stud_form.cleaned_data['date_of_birth'],
                    date_admitted           = stud_form.cleaned_data['date_admitted'],
                    mother_name             = stud_form.cleaned_data['mother_name'],
                    father_name             = stud_form.cleaned_data['father_name'],
                    mother_occ              = stud_form.cleaned_data['mother_occ'],
                    father_occ              = stud_form.cleaned_data['father_occ'],
                    last_school_att         = stud_form.cleaned_data['last_school_att'],
                    last_school_att_address = stud_form.cleaned_data['last_school_att_add'],
                    acad_status             = stud_form.cleaned_data['acad_status'],
                    privilege               = stud_form.cleaned_data['priv'],
                    year_level              = stud_form.cleaned_data['year_level']
                )
                #image_path              = request.FILES['image_path'],
                # check for name duplicates
                if not Student.objects.filter(firstname=student.firstname, lastname=student.lastname).exists():
                    #add image for student
                    if 'image_path' in request.FILES:
                        student.image_path = request.FILES['image_path']
                    student.save()
                    
                    #add bill account
                    if getRequest(request, 'submit')=="reg_bill":
                        addBillAccount(student, 'NEW')
                    
                    data['success_message'] = "New Student named '%s %s' succesfully saved" %(student.firstname, student.lastname) 
                    data['form'] = stud_form
                    
                    return render_to_response('./registration/reg_stud.html', data, context)
                else:
                    data['error_message'] = "Student named <b> %s %s </b> Already have a profile" %(stud_form['firstname'], stud_form['lastname']) 
                    return render_to_response('./registration/reg_stud.html', data, context)
                    
            else:#update
                student = Student.objects.get(studentID=getRequest(request, 'stud_id'))
                
                student.firstname               = stud_form.cleaned_data['firstname']
                student.mi                      = stud_form.cleaned_data['mi']
                student.lastname                = stud_form.cleaned_data['lastname']
                student.gender                  = stud_form.cleaned_data['gender']
                student.date_of_birth           = stud_form.cleaned_data['date_of_birth']
                student.date_admitted           = stud_form.cleaned_data['date_admitted']
                student.mother_name             = stud_form.cleaned_data['mother_name']
                student.father_name             = stud_form.cleaned_data['father_name']
                student.mother_occ              = stud_form.cleaned_data['mother_occ']
                student.father_occ              = stud_form.cleaned_data['father_occ']
                student.last_school_att         = stud_form.cleaned_data['last_school_att']
                student.last_school_att_address = stud_form.cleaned_data['last_school_att_add']
                student.acad_status             = stud_form.cleaned_data['acad_status']
                student.privilege_id            = stud_form.cleaned_data['priv']
                student.year_level              = stud_form.cleaned_data['year_level']
                
                student.save()
        else:#invalid form input values
            data['errors'] = stud_form.errors
            data['form'] = stud_form
            data['action'] = request.POST.get('action', 'add')
            return render_to_response('./registration/reg_stud.html', data, context)
    else: # display add ecit form only
        if data['action'] == 'add':
            data['form'] = StudentForm()
            return render_to_response('./registration/reg_stud.html', data, context)
        else:
            data['form'] = StudentForm
            return render_to_response('./registration/reg_stud.html', data, context)

        
#byrenx additional script for adding students
def addBillAccount(student, stud_type):
    cursor = connection.cursor()
    
    months_payable_map = { 5: 10, 6: 10, 7: 9, 8:8, 9:7, 10:6, 
                           11:5, 12:4, 1:3, 2:2, 3:1 }

    query_bills = '''SELECT psb.id, psb.item_name, psb.amount
                     FROM pis_system_billitems psb INNER JOIN
                     pis_system_assignbillitem psa 
                     ON psb.id=psa.bill_item_id_id 
                     AND psb.item_type= %s
                     WHERE psa.year_level = %s'''

    query_ins_acc = '''INSERT INTO pis_system_billaccount
                       (student_id, bill_item_name_id, balance,
                       date_added, date_fully_paid, discount, amount)
                       VALUES(%s, %s, %s, %s, %s, %s, %s)'''
    months_payable = 10 # default number of tuition months payable
    #compute months payable by the studentsx
    if stud_type=='NEW':
        month_admitted = student.date_admitted.month
        months_payable = months_payable_map[month_admitted]
        
    # get tuition payables 
    cursor.execute(query_bills, ['T', student.year_level])
    tuition = cursor.fetchone()
    # insert student tuition payables to bill_account
    if tuition is not None:
        for i in range(months_payable):
            discounted = discount(tuition[2],student.privilege.discount)
            cursor.execute(query_ins_acc,
                           [student.studentID, tuition[0], discounted, getTodaysdate(), getTodaysdate(), 0,discounted])

    #get registration fee payables
    cursor.execute(query_bills, ['R', student.year_level])
    reg_fee = cursor.fetchone()
    #insert student registration fee to billaccount
    if reg_fee is not None:
        cursor.execute(query_ins_acc, [student.studentID, reg_fee[0], reg_fee[2], getTodaysdate(), getTodaysdate(),0,reg_fee[2]])

    #get miscellaneous fee payables
    cursor.execute(query_bills+''' OR psa.year_level=0''', ['M', student.year_level])
    #insert student miscellaneous payables to bill account
    misc_fees = cursor.fetchall()
    if misc_fees is not None:
        for misc_fee in misc_fees:
            cursor.execute(query_ins_acc,
                           [student.studentID, misc_fee[0], misc_fee[2], getTodaysdate(), getTodaysdate(), 0,misc_fee[2]])

def discount(amount,percent):
    return float(amount) - ((float(percent)/100)*float(amount))   

def studentInfo(request, pk): 
    id = pk
    student = Student.objects.get(studentID = id)
    assign_item = AssignBillItem.objects.get(year_level=student.year_level,item_type='T')
    monthly_tuition_sum = 0.00
    cursor = connection.cursor()
    
    cursor.execute("SELECT count(*) from pis_system_billaccount where \
    extract(year from date_added) = %s and bill_item_name_id = %s and \
    student_id = %s and balance <> %s", [datetime.datetime.now().year,assign_item.bill_item_id_id,id,0])
    monthly_tuition_count = cursor.fetchone()[0]
    
    bills = BillAccount.objects.filter(student = id).exclude(balance=0)
    total = sum([float(x.balance) for x in bills])
  
    dis = 0.0
    if monthly_tuition_count > 4:
        if monthly_tuition_count < 10:
            dis = float(5)
        else:
            dis = float(10)
    total_due = sum([float(x.balance) for x in bills if x.bill_item_name == assign_item.bill_item_id])
    due = "{:,.2f}".format(total-((dis/100)*total_due))
    total = "{:,.2f}".format(total)

    return render_to_response( 
        './registration/student_info.html',
        { 'student'     : student,
          'system_name' : 'Enrolment System',
          'bills'       : bills, 
          'total'       : total, 
          'amount_due'  : due,
          'system_name' : SYSTEM_NAME
        },
        context_instance = RequestContext(request)
    )
    
def editStudentInfo(request, pk):
    data = {
        'action'      : '',
        'system_name' : SYSTEM_NAME
    }
    
    id = pk
    student = Student.objects.get(studentID = id)
    
    if request.POST:
        post = request.POST
        
        student.firstname               = post['firstname']
        student.mi                      = post['mi']
        student.lastname                = post['lastname']
        student.gender                  = post['gender']
        #student.date_of_birth           = post['date_of_birth']
        #student.date_admitted           = post['date_admitted']
        student.mother_name             = post['mother_name']
        student.father_name             = post['father_name']
        #student.mother_occ              = post['mother_occ']
        #student.father_occ              = post['father_occ']
        student.last_school_att         = post['prev_school']
        student.last_school_att_address = post['prev_school_address']
        student.acad_status             = post['acad_status']
        student.privilege               = post['privilege']
        student.year_level              = post['year_level']
        
        student.save()
    
    
    assign_item = AssignBillItem.objects.get(year_level=student.year_level,item_type='T')
    monthly_tuition_sum = 0.00
    cursor = connection.cursor()
    
    cursor.execute("SELECT count(*) from pis_system_billaccount where \
    extract(year from date_added) = %s and bill_item_name_id = %s and \
    student_id = %s and balance <> %s", [datetime.datetime.now().year,assign_item.bill_item_id_id,id,0])
    monthly_tuition_count = cursor.fetchone()[0]
    
    bills = BillAccount.objects.filter(student = id).exclude(balance=0)
    total = sum([float(x.balance) for x in bills])
  
    dis = 0.0
    if monthly_tuition_count > 4:
        if monthly_tuition_count < 10:
            dis = float(5)
        else:
            dis = float(10)
    total_due = sum([float(x.balance) for x in bills if x.bill_item_name == assign_item.bill_item_id])
    due = "{:,.2f}".format(total-((dis/100)*total_due))
    total = "{:,.2f}".format(total)
    
    return render_to_response( 
        './registration/student_info.html',
        { 'student'     : student,
          'system_name' : 'Enrolment System',
          'bills'       : bills, 
          'total'       : total, 
          'amount_due'  : due,
          'system_name' : SYSTEM_NAME
        },
        context_instance = RequestContext(request)
    )