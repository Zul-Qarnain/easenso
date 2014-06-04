from pis_system.models import Employee
from django.contrib.auth.models import User

class EmployeeObj(object):
    
    def getAllEmployee(self):
        query = '''SELECT pis_system_employee.*, auth_user.username,
        auth_user.first_name, auth_user.last_name, auth_user.date_joined
        FROM pis_system_employee INNER JOIN auth_user 
        ON auth_user.id=pis_system_employee.user_id 
        ORDER BY date_joined DESC'''
        return Employee.objects.raw(query);

    def getEmpInfo(self, username):
	user = User.objects.get(username=username)
        emp = Employee.objects.get(user_id=user.id)
        emp_info = {'username':username,'firstname':user.first_name, 'lastname':user.last_name, 'position':emp.position, 'address':emp.address}
        return emp_info

    def getEmpList(self, limit, offset): 
	query =  '''SELECT pis_system_employee.*, auth_user.username, 
        auth_user.first_name, auth_user.last_name, auth_user.date_joined 
        FROM pis_system_employee 
        INNER JOIN auth_user ON auth_user.id=pis_system_employee.user_id 
        ORDER BY date_joined DESC LIMIT %s OFFSET %s'''
        emp = Employee.objects.raw(query, [limit, offset])
 	return emp 
        

    def count_current_fetch(self, limit, offset):
        query = "SELECT COUNT(*) AS total FROM auth_user LIMIT %s OFFSET %s";
        c = User.objects.count(query, [limit, offset])
        return c
        


