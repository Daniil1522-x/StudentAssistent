from django import forms

from .models import Discipline


class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = ['name', 'teacher', 'course', 'hours', 'performance', 'grade', 'notes']
