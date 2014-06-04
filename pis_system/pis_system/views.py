from django.shortcuts import render, render_to_response, redirect, RequestContext

def dashboard(request):

  return render(request, 'dashboard.html', {'system_name': 'Philippine Integrated School'})