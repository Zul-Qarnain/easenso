from django.shortcuts import render_to_response, RequestContext, HttpResponse
from users import forms
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password
from users.models import User
from django.core.mail import EmailMultiAlternatives

SYSTEM_NAME = 'Easenso'

def signup_view(request):
	form    = forms.SignupForm()
	captcha = forms.CaptchaTestForm()

	return render_to_response(
		'includes/sign-up.html', 
		{ 
			'system_name' : SYSTEM_NAME + ' Sign-up',
			'form'        : form,
			'captcha'		  : captcha,
		},
		RequestContext(request),
	)

@require_POST
def signup(request):
	# try:
	captcha = forms.CaptchaTestForm(request.POST)
	form    = forms.SignupForm(request.POST)
	
	print 'GREAT!! 1'
	if form.is_valid() and captcha.is_valid():
		print 'GREAT!! 2'
		if form.cleaned_data['password'] == form.cleaned_data['confirm'] and not User.objects.filter(email__iexact = form.cleaned_data['email']).exists():
			print 'GREAT!! 3'
			user = User(
				first_name     = form.cleaned_data['firstname'],
				last_name      = form.cleaned_data['lastname'],
				username       = form.cleaned_data['username'],
				gender         = [gender for gender in request.POST['gender']][0],
				email          = form.cleaned_data['email'],
				password       = make_password(form.cleaned_data['password'], salt=None, hasher='default'),
				address        = form.cleaned_data['city'] + ', ' + form.cleaned_data['province'],
				contact_number = form.cleaned_data['mobile'],
				is_active      = True,
				user_type      = 'B',
				captcha        = captcha.cleaned_data['captcha'],
				# middle_name    = form.cleaned_data['middle_name'],	
				# date_of_birth  = form.cleaned_data['date_of_birth'],
			)

			user.save()

			subject, from_email, to_email = 'Easenso Account Validation', user.email, user.email
			text_content = ''
			html_content = "Hi %s,<br /> Thanks for signing up for Easenso!<br /> Please <a href='http://www.easenso.ph/registration/confirm_email/%s'>click this link</a> to confirm your email address. This means you will be able to reset your password if you forget it later, which is especially important if you have a paid account!<br /> If you can't click the link from your email program, please copy this URL and paste it into your web browser: <br /><br /> http://www.easenso.ph/registration/confirm_email/%s" % (user.first_name, user.email, user.email)
			message      = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
			message.attach_alternative(html_content, "text/html")
			message.send()

			print 'GREAT 4'
	# except:
	# 	return HttpResponse('Error')

	return HttpResponse('Brilliant!')

def confirm_email(request, email):
	user = User.objects.get(email__iexact = email)
	if not user.is_confirmed:
		user.is_confirmed = True
		user.save()
	else:
		pass

	return HttpResponse('Login')