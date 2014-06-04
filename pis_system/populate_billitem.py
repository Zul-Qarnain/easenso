import os
import sys

def populate():
    item = add_item('R', 'Pre School Registration', 1200)
    item = add_item('R', 'Elementary Registration', 1300)
    item = add_item('R', 'High School Registration', 1500)
    item = add_item('T', 'Pre School Monthly Tuition', 900)
    item = add_item('T', 'Elementary Monthly Tuition Grade 1 to 3', 1000)
    item = add_item('T', 'Elementary Monthly Tuition Grade 4 to 6', 1100)
    item = add_item('T', 'High School Monthly Tuition', 1300)
    item = add_item('M', 'ID', 115)
    item = add_item('M', 'Form 137', 50)
    item = add_item('M', 'Good Moral', 50)
    item = add_item('M', 'Graduation Fee', 2000)
    item = add_item('M', 'Athlete Fee', 50)
    item = add_assign_item(1,1,'R')
    item = add_assign_item(2,1,'R')
    item = add_assign_item(3,1,'R')
    item = add_assign_item(4,2,'R')
    item = add_assign_item(5,2,'R')
    item = add_assign_item(6,2,'R')
    item = add_assign_item(7,2,'R')
    item = add_assign_item(8,2,'R')
    item = add_assign_item(9,2,'R')
    item = add_assign_item(10,3,'R')
    item = add_assign_item(11,3,'R')
    item = add_assign_item(12,3,'R')
    item = add_assign_item(13,3,'R')
    item = add_assign_item(1,4,'T')
    item = add_assign_item(2,4,'T')
    item = add_assign_item(3,4,'T')
    item = add_assign_item(4,5,'T')
    item = add_assign_item(5,5,'T')
    item = add_assign_item(6,5,'T')
    item = add_assign_item(7,6,'T')
    item = add_assign_item(8,6,'T')
    item = add_assign_item(9,6,'T')
    item = add_assign_item(10,7,'T')
    item = add_assign_item(11,7,'T')
    item = add_assign_item(12,7,'T')
    item = add_assign_item(13,7,'T')
    item = add_assign_item(10,12,'M')
    item = add_assign_item(11,12,'M')
    item = add_assign_item(12,12,'M')
    item = add_assign_item(13,12,'M')
    item = add_student_priv('Paying', 0)

    print "Creating the following: "
    for b in BillItems.objects.all():
        print "- {0}".format(str(b))
def add_student_priv(priv_name, discount):
    p = StudentPrivilege.objects.get_or_create(priv_name=priv_name, discount=discount)[0]
    return p 

def add_assign_item(year_level,fk, types):
	assign_item = AssignBillItem.objects.get_or_create(bill_item_id_id=fk, year_level=year_level, item_type=types)[0]
	return assign_item

def add_item(type, name, amount):
    b = BillItems.objects.get_or_create(item_name=name, item_type=type, amount = amount)[0]
    return b

# Start execution here!
if __name__ == '__main__':
    print "Starting BillItems population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pis_system.settings')
    from pis_system.models import BillItems, AssignBillItem, StudentPrivilege
    populate()
