from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import *
from .forms import *
from pis_system.forms import ItemSearch, LogInForm
from pis_system.models import Employee, Student
from pis_objects.student import *
from pis_objects.employee import *
from helpers.helpers import *

# Create your views here.

def indexSection(request):
    context = {'form': YearLevelField()}
    return render(request, './scheduling/view_section_main.html', context)

def addSectionForm(request):
    context = {'form': SectionForm()}
    return render(request, './scheduling/add_section_form.html', context)

def indexSubject(request):
    context = {}
    return render(request, './scheduling/view_subject_main.html', context)

def addEditSubjectForm(request):
    context = {}
    return render(request, './scheduling/add_edit_subject_form.html', context)
