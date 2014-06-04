from django import forms

class LogInForm(forms.Form):
	userID = forms.CharField(
								label = '', 
								widget = forms.NumberInput(attrs = {'placeholder':'Employee ID Number'}), 
								required = True,
							)
	
	password = forms.CharField(
								label = '', 
								widget = forms.PasswordInput(attrs = {'placeholder':'Password'}), 
								required = True,
							)
	
class ItemSearch(forms.Form):
	search = forms.CharField(
								label = 'Add Item', 
								widget = forms.TextInput(attrs = {
																	'placeholder': 'Search for item to add', 
																	'class':'form-control','id':'search_student',
																}),
							)
