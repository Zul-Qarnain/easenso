from django             import forms
from pis_system.models  import *

class StudentForm(forms.ModelForm):
    GENDER = ( 
        ('', '- - - - - - - - -'),
        ('M', 'Male'),
        ('F', 'Female')
    ) 
    
    YEAR_LEVEL = (
        ('', '- - - - - - - - - - - -'),
        (1, 'Nursery'),
        (2, 'Kinder 1'),
        (3, 'Kinder 2'),
        (4, 'Grade 1'),
        (5, 'Grade 2'),
        (6, 'Grade 3'),
        (7, 'Grade 4'),
        (8, 'Grade 5'),
        (9, 'Grade 6'),
        (10, 'Grade 7'),
        (11, 'Grade 8'),
        (12, '1st Year Junior'),
        (13, '2nd Year Junior'),
        (14, '1st Year Senior'),
        (15, '2nd Year Senior')
    )
    ACAD_STATUS = (('R', 'Regular'),('I', 'Irregular'), ('T', 'Transferre'))

    studentID = forms.CharField(max_length=8,
                                widget = forms.TextInput(attrs={
                                    'class'       : 'form-control',
                                    'placeholder' : 'Enter or Generate ID',
                                    'required' : 'True',
                                }),
                )

    firstname = forms.CharField(max_length=45,
                widget = forms.TextInput(attrs={
                           'class'       : 'form-control',
                           'placeholder' : 'Enter First Name',
                           'required' : 'True'
                         }
                ), 
    )
    
    mi = forms.CharField(max_length=1,required=False,
         widget = forms.TextInput(attrs={
                    'class'       : 'form-control',
                    'placeholder' : 'Enter Middle Initial'
                  }
         ),
    )
    
    lastname = forms.CharField(max_length=45,
               widget = forms.TextInput(attrs={
                          'class'       : 'form-control',
                          'placeholder' : 'Enter Last Name',
                          'required'    : 'True',
                        }
               ), 
    )
    
    gender = forms.ChoiceField(choices = GENDER, 
                               widget=forms.Select(attrs={
                                   'class' : 'form-control'}),
    )

    date_of_birth = forms.DateField(
                    widget = forms.DateInput(format = ('%Y-%m-%d'),
                             attrs = {
                               'class' : 'form-control',
                               'required'    : 'True',
                                'placeholder': 'Year-month-day'
                             }
                    ),
    )
    date_admitted = forms.DateField(
                    widget = forms.DateInput(format = ('%Y-%m-%d'),
                             attrs = {
                               'class' : 'form-control',
                               'required'    : 'True',
                                 'placeholder': 'Year-month-day'
                             }
                    ),
    ) 
    
    father_name = forms.CharField(max_length=45,
                  widget = forms.TextInput(attrs={
                             'class'       : 'form-control',
                             'placeholder' : 'Enter Father Name',
                             'required'    : 'True',
                           }
                  ),
    )
    
    mother_name = forms.CharField(max_length=45,
                  widget = forms.TextInput(attrs={
                             'class'       : 'form-control',
                             'placeholder' : 'Enter Mother Name',
                             'required'    : 'True',
                           }
                  ),
    )
    
    father_occ = forms.CharField(max_length=45,
                 widget = forms.TextInput(attrs={
                             'class'       : 'form-control',
                             'placeholder' : 'Enter Father Occupation',
                             'required'    : 'True',
                           }
                 ),
    ) 
    
    mother_occ = forms.CharField(max_length=45,
                 widget = forms.TextInput(attrs={
                             'class'       : 'form-control',
                             'placeholder' : 'Enter Mother Occupation',
                             'required'    : 'True',
                           }
                  ),
    )  
    
    last_school_att = forms.CharField(max_length=100,
                      widget = forms.TextInput(attrs={
                                 'class' : 'form-control',
                                 'required'    : 'True',
                               }
                      ),
    )
    
    last_school_att_add = forms.CharField(max_length=100,
                          widget = forms.TextInput(attrs={
                                     'class' : 'form-control',
                                     'required'    : 'True',
                                   }
                          ), 
    )
    
    acad_status = forms.ChoiceField(choices = ACAD_STATUS,
                                    widget = forms.Select(attrs={
                                        'class': 'form-control'
                                    })
    )

    image_path  = forms.FileField(required=False)

    priv = forms.ModelChoiceField(queryset=StudentPrivilege.objects.all(),
                                  widget = forms.Select(attrs={
                                      'class' : 'form-control'
                                  })
    )
    
    year_level = forms.ChoiceField(choices = YEAR_LEVEL,
                                   widget = forms.Select(attrs={
                                       'class' : 'form-control',
                                   })
    )

    class Meta:
        model = Student
        exclude = ['subjects']


class SearchForm(forms.Form):
    OPTIONS = ( 
        ('studentID', 'ID Number'),
        ('firstname', 'Firstname'),
        ('lastname', 'Lastname')
    )
    
    options = forms.ChoiceField(choices = OPTIONS)

    search = forms.CharField(widget= forms.TextInput(attrs={
        'class':'form-control',
        'required': 'required'})
    )
