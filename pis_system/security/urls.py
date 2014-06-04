from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static
from security.views import *

urlpatterns = patterns('',
    url(r'^login', loginForm),
    url(r'^logout$', logout, {'next_page':'/login'}),
    url(r'^validate_user', validateUserLogin),                       
    url(r'^employee_search', employeeSearch),
    url(r'^employee_view', employeeView),
    url(r'^employee_profile', employeeProfile),
    url(r'^addedit_employee', addEditEmployee),
    url(r'^generate_employee_id', genEmpID),
)
