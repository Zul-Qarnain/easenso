import sys
from django.db import connection
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from pis_system.forms import *
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from pis_system.models import (
    Student, 
    Employee,
    BillAccount, 
    BillItems, 
    Packages,
    User,
    BillPackage,
    Transaction,
    TransactionBreakdown,
    OneOffAccount,
    OneOffTransaction,
    AssignBillItem
  )
SYSTEM_NAME = 'Billing'
@login_required(login_url='/login')
def others(request):
  if 'payee' in request.GET:
    #rs = BillItems.objects.filter(item_type='O')
    payee = request.GET.get('payee')
    bills = OneOffAccount.objects.select_related('billitems').filter(payee=payee, paid=False)
    total = 0 
    for bill in bills:
      total = total + bill.bill_item_name.amount 
    if 'search' in request.GET:
      rs = BillItems.objects.all()
      filter = request.GET.get('item_search_filters')    
      query_copy = request.GET.copy()
      if 'query' in request.GET:
        if filter == "item_code":
          rs = rs.filter(id=filter)
        if filter == "item_name":
          rs = rs.filter(item_name=filter)
          
      rs = rs.filter(item_type='O')      
      
      return render(request, './billing/others.html', {'payee':payee, 'rs':rs, 'query_copy':query_copy, 'bills':bills, 'total':total, 'system_name': SYSTEM_NAME})
    return render(request, './billing/others.html', {'payee':payee, 'bills':bills, 'total':total, 'system_name': SYSTEM_NAME})
    
  return render(request,'./billing/others.html', {'system_name': SYSTEM_NAME})

@login_required(login_url='/login')
def student(request):
  if 'submit' in request.GET:
    return search_student(request)
  return render(request,'./billing/index.html', {'system_name': SYSTEM_NAME})

def login(request):
    
    form=LogInForm()
    redirect_to = '/dashboard'
    system = 'Dashboard'
    names = {
      '/dashboard':'Dashboard', 
      '/billing/student':'Billing',
      '/billing/':'Billing'
      
      }
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
          user = auth.authenticate(username=form.cleaned_data['userID'], password=form.cleaned_data['password'])
          
          if user is not None and user.is_active:
            auth.login(request,user)
            students=Student.objects.get_queryset()
            
            if 'next' in request.GET:
              redirect_to = request.GET.get('next')
            return redirect(redirect_to)
          
    if 'next' in request.GET:
      redirect_to = request.GET.get('next')
      system = names[redirect_to]
      
    return render(
                  request,
                  'login.html',
                  {
                      'form': form,
                      'system_name': system
                  }
                )

@login_required(login_url='/billing')
def search_student(request):
  try:
    user = User.objects.get(username=request.user)
    search = request.GET.get('search_student')
    type = request.GET.get('student_search_filter')
    size = Student.objects.all().count()
    
    total=0
    if type == 'id_num':
      students = Student.objects.filter(studentID__contains=search)
      total = students.count
    elif type == 'last_name':
      students = Student.objects.filter(lastname__istartswith=search)
      total = students.count
    elif type == 'first_name':
      students = Student.objects.filter(firstname__istartswith=search)
      total = students.count
    queries_without_page = request.GET.copy()
    if queries_without_page.has_key('page'):
        del queries_without_page['page']
    
    paginator = Paginator(students, 3)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        students = paginator.page(page)
    except (InvalidPage, EmptyPage):
        students = paginator.page(paginator.num_pages)
  except:
    print sys.exc_info()[0], sys.exc_info()[1]
  return render(request,'billing/index.html', { 'system_name': SYSTEM_NAME, 'query_params':queries_without_page, 'user': user,'students': students ,'total': total, 'size':size})

@login_required(login_url='/billing')
def get_student(request):

  context = RequestContext(request)
  getstud = request.GET.get('student')
  try:
    student=Student.objects.get(studentID = getstud)
    
  except:
    print sys.exc_info()[0], sys.exc_info()[1]

  return render_to_response('stub.html', {'student': student}, context)

@login_required(login_url='/billing')
def get_bill(request, *args):
  
  context = RequestContext(request)
  cursor = connection.cursor()
  try:
    if args:
      id = args[0]
    else:
      id = request.GET.get('student')
    total=0.00
  

    student_id = Student.objects.get(studentID=id)
    assign_item = AssignBillItem.objects.get(year_level=student_id.year_level,item_type='T')
    monthly_tuition_sum = 0.00
  except:
    print sys.exc_info()[0], sys.exc_info()[1]
  try:
    cursor.execute("SELECT count(*) from pis_system_billaccount where \
    extract(year from date_added) = %s and bill_item_name_id = %s and \
    student_id = %s and balance <> %s", [datetime.datetime.now().year,assign_item.bill_item_id_id,id,0])
    monthly_tuition_count = cursor.fetchone()[0]
    
    bills = BillAccount.objects.filter(student = id).exclude(balance=0)
    total=sum([float(x.balance) for x in bills])
 #   monthly_tuition_sum = sum([float(x.balance) for x in bills if x.bill_item_name.item_type == 'T'])

    student=Student.objects.get(studentID=id)
#    name_monthly = AssignBillItem.objects.get(item_type='T',year_level=student.year_level)  
    dis = 0.0
    if monthly_tuition_count > 4:
        if monthly_tuition_count < 10:
            dis = float(5)
        else:
            dis = float(10)
    total_due = sum([float(x.balance) for x in bills if x.bill_item_name == assign_item.bill_item_id])
    due = "{:,.2f}".format(total-((dis/100)*total_due))
    total = "{:,.2f}".format(total)
    # loop_times = [i+1 for i in range(10 - monthly_tuition_count)]
     
  except:
    print sys.exc_info()[0], sys.exc_info()[1]
 
  print "GOT ", student.studentID
#  data = render_to_response('billing/billing_info.html', {'monthly_tuition_sum':monthly_tuition_sum,'monthly_name':name_monthly.bill_item_id.item_name,'bills': bills, 'total':total, 'amount_due':due}, context)
  data = render_to_response('billing/billing_info.html', {'studentID':student.studentID, 'bills': bills, 'total':total, 'amount_due':due}, context)
  return data
    
@login_required(login_url='/billing')
def get_suggestions(request):
  
  context = RequestContext(request)
  cursor = connection.cursor()

  type = request.GET.get('query_type')
  query = request.GET.get('query')
  student_id = request.GET.get('student')

  student = Student.objects.get(studentID=student_id)
  assign_bill_item = AssignBillItem.objects.get(year_level=student.year_level,item_type='T')

  cursor.execute("SELECT count(*) from pis_system_billaccount where \
    extract(year from date_added) = %s and bill_item_name_id = %s and \
    student_id = %s", [datetime.datetime.now().year,assign_bill_item.bill_item_id_id,student_id])
  monthly_tuition_count = cursor.fetchone()[0]

  #monthly_tuition_count = BillAccount.objects.filter(student=student, bill_item_name = assign_item.bill_item_id,date_added='2015').count()
  #b=BillAccount.objects.filter(student=student).exclude(balance=0.00)
  student = Student.objects.get(studentID=student)
  #assign_bill_item = AssignBillItem.objects.get(year_level=student.year_level, item_type='T')

  if type == 'item_name':
        rs = BillItems.objects.filter(item_name__contains=query)#.exclude(id__in=[o.bill_item_name_id for o in b if o.bill_item_name.item_type == 'T'  ])
  elif type == 'item_code':
        rs = BillItems.objects.filter(id__contains=query)#.exclude(id__in=[o.bill_item_name_id for o in b if o.bill_item_name.item_type == 'T' ] )
  elif type == 'package_name':
    rs = Packages.objects.filter(item_name__contains=query)
  #rs = BillItems.objects.all()
  #rs.filter(assign = student.year_level)
  not_allowed = AssignBillItem.objects.only('bill_item_id').exclude(year_level = student.year_level).distinct('bill_item_id')
  allowed = AssignBillItem.objects.only('bill_item_id').filter(year_level = student.year_level).distinct('bill_item_id')
  not_allowed = not_allowed.exclude(bill_item_id__in = [b.bill_item_id_id for b in allowed])
  rs = rs.exclude(pk__in = [b.bill_item_id_id for b in not_allowed])
  
  if monthly_tuition_count >= 10:
    rs = rs.exclude(item_type = 'T')
  
  return render_to_response('billing/bill_suggestions.html', {'rs':rs})

@login_required(login_url='/billing')  
def bill_student(request):
  
  context = RequestContext(request)
  bill = request.GET.get('bill')
  student = request.GET.get('student')
  count = request.GET.get('count')
  type = request.GET.get('query_type')
  try:
    if BillItems.objects.filter(id=bill).exists(): 
      add_bill_account(student, bill)     
  except:
    print "error bill student",sys.exc_info()[0], sys.exc_info()[1]
  return get_bill(request)

def add_bill_account(student_id, bill):
  cursor = connection.cursor()
  
  student = Student.objects.get(studentID=student_id)
  if student.privilege != 0:
       discount = student.privilege.discount
  bill_item = BillItems.objects.get(id=bill)  
  if bill_item.item_type == 'T':
      amount = float(bill_item.amount)-((discount/100)*float(bill_item.amount))
      cursor.execute("SELECT count(*) from pis_system_billaccount where \
      extract(year from date_added) = %s and bill_item_name_id = %s and \
      student_id = %s", [datetime.datetime.now().year,bill,student_id])
      monthly_tuition_count = cursor.fetchone()[0]
      if monthly_tuition_count < 10:
        acct = BillAccount(student_id=student_id, bill_item_name_id=bill, balance=amount, amount=amount)
        return acct.save()
  else:
      acct = BillAccount(student_id=student_id, bill_item_name_id=bill, balance=bill_item.amount, amount=bill_item.amount)
      return acct.save()

@csrf_protect
def add_bill(request):

  if request.method == 'POST':  
    context = RequestContext(request)
    items = request.POST.getlist('items[]')
    payee = request.POST.get('payee')
    type = request.POST.get('query_type')
    total = 0
    try:    
      user = Employee.objects.get(user_id=request.user.id)
      
      for bill in items:
        bill_item = BillItems.objects.get(id=bill)

        acct = OneOffAccount.objects.create(
          payee = payee,
          bill_item_name = bill_item
          )
      bills = OneOffAccount.objects.select_related('billitems').filter(payee=payee, paid=False)
      for bill in bills:
        total = total + bill.bill_item_name.amount   
    except:
      print "error add bill",sys.exc_info()[0], sys.exc_info()[1],
    return render_to_response( './billing/oneoff_bill.html', { 'bills':bills, 'total':total} , context)
 
@csrf_protect  
def transact(request):

  items = request.POST.getlist("items[]")
  cash = request.POST.get("tender")
  total = request.POST.get("total")
  user = request.user.id
  discount = request.POST.get("discount")
  studentID = request.POST.get("studentID")
  print 'student ', studentID
  try:
    employee= Employee.objects.get(user_id=user)
  except:
    print "error employee", sys.exc_info()[0], sys.exc_info()[1]
  try:
    total = float(total)
    cash = float(cash)
    transaction = Transaction(amount_due=cash, cashier_id=employee.id, student=studentID)
    transaction.save()
    print 'transaction saved'
    for id in items:
      breakdown = TransactionBreakdown(transaction_id_id=transaction.id, bill_account_id_id=id)
      breakdown.save()
      acct = BillAccount.objects.get(id=id)
      acct.balance = 0
      if acct.bill_item_name.item_type == 'T':
          acct.discount =float(discount)
          acct.amount = float(acct.amount) - ((float(discount)/100)*float(acct.amount))
      id = acct.student_id
      acct.save()
  except:
    print "error items transact", sys.exc_info()[0], sys.exc_info()[1]
  data = get_bill(request, (id))
  return data

  
@csrf_protect  
def transact_one(request):

  items = request.POST.getlist("items[]")
  cash = request.POST.get("tender")
  total = request.POST.get("total")
  user = request.user.id
  context = RequestContext(request)
  try:
    employee= Employee.objects.get(user_id=user)
  except:
    pass
  try:
    total = float(total)
    cash = float(cash)
    transaction = Transaction(amount_due=cash, cashier_id=employee.id)
    transaction.save()
  
    for id in items:
      breakdown = OneOffTransaction(transaction_id=transaction.id, acct_id=id)
      breakdown.save()
      acct = OneOffAccount.objects.get(id=id)
      acct.paid = True
      acct.save()
    payee = acct.payee
    bills = OneOffAccount.objects.select_related('billitems').filter(payee=payee, paid=False)
    total = 0 
    for bill in bills:
      total = total + bill.bill_item_name.amount
  except:
    print "error", sys.exc_info()[0], sys.exc_info()[1]

  data = render_to_response('./billing/oneoff_bill.html', {'payee':payee, 'bills':bills, 'total':total}, context)
  
  return data  

@csrf_protect  
def get_history_transaction(request):
    context = RequestContext(request)
    student_id = request.GET.get('student')
    transaction = Transaction.objects.filter(student=student_id)

    data = render_to_response('billing/transaction_history.html', {'transactions':transaction}, context)
    return data

@csrf_protect 
def get_item_history_transaction(request):
    context = RequestContext(request)
    transact_id = request.GET.get('transact_id')
    transaction = TransactionBreakdown.objects.filter(transaction_id=transact_id)
    total = Transaction.objects.get(id=transact_id)
    total = total
    data = render_to_response('billing/transaction_item_history.html', {'transactions':transaction,'total':total}, context)
    return data
