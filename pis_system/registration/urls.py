from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static
from registration.views import *


urlpatterns = patterns('',
#    url(r'^validate_user$', registration),
    url(r'^$', registration),
    url(r'^regStud?', regStud), #edit
    url(r'^searchRegStud?', searchRegStudents),
    url(r'^generate_student_id', genStudentID), #edit
    url(r'^viewStudentInfo/(?P<pk>\d+)/?', studentInfo),
    url(r'^editStudentInfo/(?P<pk>\d+)/?', editStudentInfo)
)
