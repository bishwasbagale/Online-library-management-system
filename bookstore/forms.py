
from cProfile import label
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.forms import ModelForm
from bookstore.models import Chat, Book

from django import forms



class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('message', )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher', 'year', 'uploaded_by', 'desc','pdf','cover')        


class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        error_messages = {'username':{'required':'please enter username'},
                          'first_name':{'required':'please enter first_name'},
                          'last_name':{'required':'please enter last_name'},
                          'email':{'required':'please enter email'},
                          'password':{'required':'please enter password'}}
        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            }


      
class changepassword(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',label_suffix=' ', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',label_suffix=' ',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password',label_suffix=' ',widget=forms.PasswordInput(attrs={'class':'form-control'}))

      

        
        