from django.forms import ModelForm
from django import forms
from models import OrganizationHash
from models import Discuss

class UploadFileForm(forms.Form):
	filename = forms.CharField(max_length=50)

class UserForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50)

class NewUserForm(forms.Form):
	nickname = forms.CharField(max_length=50)
	emailUser = forms.CharField(max_length=50)
	passUser = forms.CharField(max_length=50)



class UrlForm(forms.Form):
	urlProject = forms.CharField(max_length=80)

class UpdateForm(forms.Form):
	newPass = forms.CharField(max_length=50)
	newEmail = forms.CharField(max_length=50)
#	choiceAvatar = forms.ChoiceField(choices=AVATAR_CHOICES, widget=forms.RadioSelect()

class TeacherForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    hashkey = forms.CharField(max_length=50)
    #classroom = forms.CharField(max_length=50)

class OrganizationHashForm(ModelForm):
    class Meta:
        model = OrganizationHash
        fields = ['hashkey']

class OrganizationForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    hashkey = forms.CharField(max_length=70)


class CoderForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    password_confirm = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    email_confirm = forms.CharField(max_length=50)
    birthmonth = forms.CharField(max_length=50)
    birthyear = forms.CharField(max_length=50)
    gender = forms.CharField(max_length=50)
    #gender_other = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)



class LoginOrganizationForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

class LoginCoderForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)


class DiscussForm(forms.Form):
    comment = forms.CharField(help_text="Please, write your comment.")

    class Meta:
        model = Discuss
