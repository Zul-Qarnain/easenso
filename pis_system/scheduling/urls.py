from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = patterns('',
                       url(r'^section', indexSection),
                       url(r'^add_edit_section', addSectionForm),
                       url(r'^subject', indexSubject),
                       url(r'^add_edit_subject', addEditSubjectForm),
)
