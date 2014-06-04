from django import forms
from django.contrib.auth.models import *
from pis_system.models import Employee

class UserForm(forms.Form):
    username = forms.CharField(required=True, max_length=5,
                              widget=forms.TextInput(attrs={
                                  'class':'form-control',
                                  'placeholder':'Type or Generate ID',
                                  'required':'True'
                              })
    )
    first_name = forms.CharField(widget=forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'Firstname', 'required':'True'}), required=True)
    last_name = forms.CharField( widget=forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'Lastname', 'required':'True'}), required=True)
    
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                    widget=forms.Select(attrs= {
                        'class': 'form-control'
                    }) 
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    
class EmployeeForm(UserForm):
    position = forms.CharField( widget=forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'Position', 'required': 'True'}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'Address'}))
    image_path = forms.FileField(required=False)
    
    class Meta:
        model = Employee
        fields = ['position', 'address', 'image_path']
    
    
    

    
    
    



