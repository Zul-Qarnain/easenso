from django import forms
from .models import User
from captcha.fields import CaptchaField
from functools import partial

DateInput = partial(
	forms.DateInput, 
	{
		'class'    : 'form-control',
		'id'       : 'date-of-birth',
		'required' : 'True',
	}
)

class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()

class SignupForm(forms.Form):

	firstname = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'First Name',
				'class'       : 'form-control',
				'id' 				  : 'first-name',
				'required'    : 'True',
			}
		),
	)

	lastname = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Last Name',
				'class'       : 'form-control',
				'id'			    : 'last-name',
				'required'    : 'True',
			}
		),
	)

	# GENDER = [
	#   ('M', 'Male'),
	#   ('F', 'Female'),
	# ]

	# gender = forms.ChoiceField(
	#   label = '',
	#   choices = GENDER,
	#   widget   = forms.Select(
	#     attrs = {
	#       'placeholder' : 'Address',
	#       'class'       : 'form-control',
	#       'id'          : 'gender',
	#       'maxlength'   : 50,
	#       'type'        : 'text',
	#       'required'    : 'True',
	#       }
	#   ),
	# )

	username = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Username Desired',
				'class'       : 'form-control',
				'id'			    : 'signup-username',
				'required'    : 'True',
			}
		),
	)

	password = forms.CharField(
		widget = forms.PasswordInput(
			attrs = {
				'placeholder' : 'Enter Password',
				'class'       : 'form-control',
				'id'			    : 'signup-password',
				'required'    : 'True',
			}
		),
	)

	confirm = forms.CharField(
		widget = forms.PasswordInput(
			attrs = {
				'placeholder' : 'Re-type Password',
				'class'       : 'form-control',
				'id'			    : 'password-confirm',
				'required'    : 'True',
			}
		),
	)


	email = forms.EmailField(
		label    = '', 
		widget   = forms.TextInput(
			attrs = {
				'placeholder' : 'Email address',
				'class'       : 'form-control',
				'id'          : 'email-address',
				'type'        : 'email',
				'required'    : 'True',
			}
		),
	)

	mobile = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Mobile Number',
				'class'       : 'form-control',
				'id'			    : 'mobile-num',
				'required'    : 'True',
			}
		),
	)

	city = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'City',
				'class'       : 'form-control',
				'id'			    : 'city',
				'required'    : 'True',
			}
		),
	)

	province = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Province',
				'class'       : 'form-control',
				'id'			    : 'province',
				'required'    : 'True',
			}
		),
	)

	# date_of_birth = forms.DateField(
	# 	widget=DateInput()
	# )