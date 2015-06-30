from django.shortcuts import render_to_response, RequestContext, HttpResponse
# from django.http import  HttpResponseRedirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required


SYSTEM_NAME = 'Easenso'

def index(request):
  return render_to_response(
    'intro/pre-registration.html', 
    { 
      'system_name'       : SYSTEM_NAME,
    },
    RequestContext(request)
  )
    
# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect('/')