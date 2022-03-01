from django import forms
from django.contrib.auth.models import User
from django.forms import fields, widgets
from student.models import Student
from moderator.models import Moderator
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserCreateForm(UserCreationForm):
    clg_reg_no = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'College Registration Number',}),)
    graduation_year = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder':'Graduation Year',}),)
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-user', 'type':'tel', 'placeholder':'Phone: ex  +91XXXXXXXXXX', 'pattern':'[+][0-9]{2}[0-9]{10}'}),)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'Username',}),
            'first_name': forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'First Name',}),
            'last_name': forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'Last Name',}),
            'email': forms.EmailInput(attrs={'class':'form-control form-control-user', 'placeholder':'Email',}),
            # 'password1': forms.PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder':'Password', 'name':'password', 'id':'password'}),
            # 'password2': forms.PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder':'Confirm_password', 'name':'Confirm_password', 'id':'Confirm_password'}),
            # 'clg_reg_no': forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'College Registration Number',}),
            # 'graduation_year': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder':'Graduation Year',}),
            # 'phone': forms.TextInput(attrs={'class':'form-control form-control-user', 'type':'tel', 'placeholder':'Phone: ex  +91XXXXXXXXXX', 'pattern':'[+][0-9]{2}[0-9]{10}'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder':'Password','onkeyup':'check();'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder':'Confirm Password','onkeyup':'check();'})

    def save(self, commit=True):
        # if not commit:
        #     raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UserCreateForm, self).save(commit=True)
        user_profile = Student(
        user=user,
        clg_reg_no=self.cleaned_data['clg_reg_no'],
        graduation_year=self.cleaned_data['graduation_year'],
        phone=self.cleaned_data['phone'],
        )
        user_profile.save()
        return user

    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
       return self.cleaned_data

class UserProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(attrs={'id':'file','type':'file','onchange':'loadFile(event)'}), required=False)
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','email']
        widgets ={
            'username': forms.TextInput(attrs={'class':'form-control ', 'id':'username', 'placeholder':'Username',}),
            'first_name': forms.TextInput(attrs={'class':'form-control ', 'id':'first_name', 'placeholder':'First Name',}),
            'last_name': forms.TextInput(attrs={'class':'form-control ', 'id':'last_name', 'placeholder':'Last Name',}),
            'email': forms.EmailInput(attrs={'class':'form-control ', 'id':'email', 'placeholder':'Email','readonly':'true'}),
        }

    def save(self, commit=True):
        # return super().save()
        user =  super().save(commit=commit)
        l = user.groups.values_list('name', flat=True) # getting user groups query set
        groups = list(l)  # adding them to the list
        photo = self.cleaned_data.get('photo')
        if photo is not None:
            if 'moderator' in groups:
                user_profile = Moderator.objects.get(user = user)
                user_profile.photo = photo
            else:
                user_profile = Student.objects.get(user = user)
                user_profile.photo = photo
            user_profile.save()
        return user
