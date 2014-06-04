from django             import forms
from pis_system.models  import *


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'year_level', 'adviser', 'room_no', 'capacity']


class YearLevelField(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['year_level']
