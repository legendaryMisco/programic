from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Student,ContactForm


class createAccountForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(createAccountForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
            
            
class EditAccountForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['user']
        
    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        
            
class StudentContactForm(ModelForm):
    class Meta:
        model = ContactForm
        exclude = ['']
        
    def __init__(self, *args, **kwargs):
        super(StudentContactForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control border-top-0 border-right-0 border-left-0 p-0'})
        