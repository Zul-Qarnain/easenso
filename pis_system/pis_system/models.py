from django.db import models
from django.contrib.auth.models import User

YEAR_LEVEL = ((1,'Nursery'),
              (2,'Kinder 1'),
              (3,'Kinder 2'),
              (4,'Grade 1'),
              (5,'Grade 2'),
              (6,'Grade 3'),
              (7,'Grade 4'),
              (8,'Grade 5'),
              (9,'Grade 6'),
              (10,'Grade 7'),
              (11,'Grade 8'),
              (12,'1st Year Junior'),
              (13,'2nd Year Junior'),
              (14,'1st Year Senior'),
              (15,'2nd Year Senior')
             )

GRADING_PERIODS = ((1, '1st Grading'),
                   (2, '2nd Grading'),
                   (3, '3rd Grading'),
                   (4, '4th Grading'),
                   (5, 'Final')
                  )
class Employee(models.Model):
    user = models.OneToOneField(User)
    position = models.CharField(max_length=45)
    address = models.CharField(max_length=100, blank=True)
    image_path = models.FileField(upload_to='employees')

    def __unicode__(self):
      return self.user.username




#ok
# class Employee(models.Model):
#     employeeID = models.CharField(max_length=9, primary_key=True)
#     firstname = models.CharField(max_length=45)
#     mi = models.CharField(max_length=1)
#     lastname = models.CharField(max_length=45)
#     position = models.CharField(max_length=45)
#     address = models.CharField(max_length=100, blank=True)
#     image_path = models.FileField(upload_to='templates/static/images/employees/')

#     def __unicode__(self):
#       return self.employeeID
# #ok
# class EmployeeAccount(models.Model):
#     PRIVILEGES = ((1,'Admin'),
#                   (2,'Coordinator'),
#                   (3,'Adviser'),
#                   (4,'Finance'),
#                   (5,'Registrar')
#                  )
#     employee = models.ForeignKey(Employee)
#     password = models.CharField(max_length=45)
#     date_created = models.DateTimeField(auto_now=True, auto_now_add=True)
#     account_privilege = models.IntegerField(choices=PRIVILEGES)

#     def __unicode__(self):
#       return unicode(self.employee)
#ok    
class StudentPrivilege(models.Model):
    priv_name = models.CharField(max_length=100)
    discount = models.FloatField(max_length=3)
    date_created = models.DateField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
     return self.priv_name
#ok
class Subject(models.Model):
    title = models.CharField(max_length=45)
    units = models.IntegerField()

    def __unicode__(self):
      return self.title

#ok
class Student(models.Model):
    ACAD_STATUS = (('R', 'Regular'),('I', 'Irregular'), ('T', 'Transferre'))
    GENDERS = (('M', 'Male'),('F', 'Female'))
    studentID = models.CharField(max_length=9, primary_key=True)
    firstname = models.CharField(max_length=45)
    mi = models.CharField(max_length=1)
    lastname = models.CharField(max_length=45)
    gender = models.CharField(max_length=1, choices=GENDERS)
    date_of_birth = models.DateField()
    date_admitted = models.DateField()
    mother_name = models.CharField(max_length=45) 
    father_name = models.CharField(max_length=45)
    mother_occ = models.CharField(max_length=45, blank=True)  # mother occupation
    father_occ = models.CharField(max_length=45, blank=True)  # father occupation
    last_school_att = models.CharField(max_length=100, blank=True)
    last_school_att_address = models.CharField(max_length=100, blank=True)
    acad_status = models.CharField(max_length=45, choices=ACAD_STATUS)
    image_path = models.FileField(upload_to='students')
    privilege = models.ForeignKey(StudentPrivilege, blank=True, null=True)
    year_level = models.IntegerField(choices=YEAR_LEVEL)
    subjects = models.ManyToManyField(Subject, through='StudentSubjects')

    def __unicode__(self):
      return self.studentID
#ok
class BillItems(models.Model):
    ITEM_TYPES = (('R',"Registration"),('T',"Tuition"),('M',"Miscellaneous"), ('O',"Others"))
    item_name = models.CharField(max_length=45)
    item_type = models.CharField(max_length=1, choices=ITEM_TYPES)
    amount  = models.DecimalField(max_digits=7, decimal_places=2)
   # date_created = models.DateField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
      return self.item_name

class AssignBillItem(models.Model):
    ITEM_TYPES = (('R',"Registration"),('T',"Tuition"),('M',"Miscellaneous"), ('O',"Others"))
    bill_item_id = models.ForeignKey(BillItems)
    year_level = models.IntegerField(choices=YEAR_LEVEL)
    item_type = models.CharField(max_length=1, choices=ITEM_TYPES)


    def __unicode__(self):
      return self.year_level
#ok
class BillAccount(models.Model):
    student = models.ForeignKey(Student)
    bill_item_name = models.ForeignKey(BillItems)
    balance = models.DecimalField(max_digits=9, decimal_places=2)
    date_added = models.DateField(auto_now=True, auto_now_add = True)
    date_fully_paid = models.DateField(auto_now=True, auto_now_add = True)
    discount = models.FloatField(max_length=3, default=0)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __unicode__(self):
      return unicode(self.student)

class Transaction(models.Model):
    amount_due = models.DecimalField(max_digits=9,decimal_places=2)
    date_transacted = models.DateTimeField(auto_now_add=True)
    cashier = models.ForeignKey(Employee)
    student = models.CharField(max_length=45)

    def __unicode__(self):
      return unicode(self.date_transacted)
      
class TransactionBreakdown(models.Model):
    transaction_id = models.ForeignKey(Transaction)
    bill_account_id = models.ForeignKey(BillAccount)

class Packages(models.Model):
    item_name = models.CharField(max_length=20)

    def __unicode__(self):
      return unicode(self.item_name)

class BillPackage(models.Model):
    bill_item = models.ForeignKey(BillItems)
    package_id = models.ForeignKey(Packages)
    date_added = models.DateField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
      return unicode(self.package_id)

class OneOffAccount(models.Model):
 
    payee = models.CharField(max_length=45)
    bill_item_name = models.ForeignKey(BillItems)
    paid = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
      return self.payee
      
class OneOffTransaction(models.Model):
    transaction = models.ForeignKey(Transaction)
    acct = models.ForeignKey(OneOffAccount)    
     
#ok
class Section(models.Model):
    name = models.CharField(max_length=45)
    year_level = models.IntegerField(choices=YEAR_LEVEL)
    room_no = models.IntegerField()
    students = models.ManyToManyField(Student, through='StudentSection')
    advisers = models.ManyToManyField(Employee, through='AdviserSection')

    def __unicode__(self):
      return self.name

#StudentSection
class StudentSection(models.Model):
    student = models.ForeignKey(Student)
    section = models.ForeignKey(Section)
    school_year = models.CharField(max_length=20)

    def __unicode__(self):
      return unicode(self.student)
#ok
class AdviserSection(models.Model):
    employee = models.ForeignKey(Employee)
    section = models.ForeignKey(Section)
    school_year = models.CharField(max_length=20)

    def __unicode__(self):
      return unicode(self.employee)

#ok
class StudentSubjects(models.Model):
    subject = models.ForeignKey(Subject)
    student = models.ForeignKey(Student)
    teacher = models.ForeignKey(Employee)
    year_level = models.IntegerField(choices=YEAR_LEVEL)
    school_year = models.CharField(max_length=20)
    time_begin = models.TimeField()
    time_end = models.TimeField()
    #days could be M - Monday, T-Tuesday ,W-Wednesday,
    #TH-Thursday, F-Friday, ST-Saturday, S-Sunday
    days = models.CharField(max_length=15)

    def __unicode__(self):
      return self.student
#ok
class StudentGrade(models.Model):
    student_subject = models.ForeignKey(StudentSubjects)
    grading_period = models.IntegerField(choices=GRADING_PERIODS)
    grade = models.IntegerField()

#ok
class CharacterRate(models.Model):
   
    character_choices = (('C','Cleanliness'),
                         ('CP','Courtesy and Politeness'),
                         ('HC','Helpfulness and Cooperativeness'),
                         ('I','Industriousness'),
                         ('LI','Leadership and Innitiative'),
                         ('O','Obedience'),
                         ('SC','Self Control'),
                         ('PP','Promptness and Punctuality'),
                         ('S','Sportmanship'),
                         ('TE','Thrift and Economy'),
                         ('MS','Modesty and Simplicity')
                        )

    student = models.ForeignKey(Student)
    rate = models.FloatField(max_length=3)
    character = models.CharField(max_length=2,choices=character_choices)
    year_level = models.IntegerField(choices=YEAR_LEVEL)
    school_year = models.CharField(max_length=25)
    period = models.IntegerField()
    date_rated = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
      return self.student
#ok
class Attendance(models.Model):
    MONTHS = ((1, 'January'),
              (2, 'February'),
              (3, 'March'),
              (4, 'April'),
              (5, 'May'),
              (6, 'June'),
              (7, 'July'),
              (8, 'August'),
              (9, 'September'),
              (10, 'October'),
              (11, 'November'),
              (12, 'December')
             )
    student = models.ForeignKey(Student)
    year_level = models.IntegerField()
    school_year = models.CharField(max_length=20)
    no_school_days = models.IntegerField()
    no_school_days_tardy = models.IntegerField()
    no_school_days_present = models.IntegerField()
    month = models.IntegerField(choices=MONTHS)

    def __unicode__(self):
      return self.student
    

    
    
