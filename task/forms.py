
from django import forms
from .models import Task


class DateInput(forms.DateInput):
    input_type = 'date'

class AddTaskForm(forms.ModelForm):

    title = forms.CharField(
        label='Title', help_text='Required')
    description = forms.Textarea()
    file = forms.ImageField(
        label='File', required=False)

 

    class Meta:
        model = Task
        fields = ( 'user' ,'title', 'description', 'dueDate', 'file')
        widgets = {
            'dueDate': DateInput(),
            'user': forms.TextInput(attrs={'value': '', 'id': 'id', 'type': 'hidden'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = self.fields['title'].label
        self.fields['description'].widget.attrs['placeholder'] = self.fields['description'].label
        self.fields['file'].widget.attrs.update({'class': 'fileupload'})

   
