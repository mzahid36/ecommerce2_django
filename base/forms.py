from django import forms
from django.contrib.auth.forms import AuthenticationForm,UsernameField,UserCreationForm,PasswordChangeForm,PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth.models import User
from .models import Customer,Address, BookTable
from django.contrib.auth import password_validation



# user registreation
class UserRegistration(UserCreationForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class UserLogin(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control','style':'color: #ff6426'}))
    password = forms.CharField(label=_('Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control','style':'color: #ff6426'}))

class passwordchange(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_('New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new passord','class':'form-control'}))

class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class NewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("Enter New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class UserProfile(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','email','phone','gender','profile_pic']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'})
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['division','district','thana','holding_street_village','zipcode']
        widgets = {
            'division': forms.Select(attrs={'class':'form-control'}),
            'district': forms.TextInput(attrs={'class':'form-control'}),
            'thana':forms.TextInput(attrs={'class':'form-control'}),
            'holding_street_village':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.TextInput(attrs={'class':'form-control'}),
        }



class BookTableForm(forms.ModelForm):
    class Meta:
        model = BookTable
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'persons':forms.Select(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'note':forms.Textarea(attrs={'class':'form-control'}),
            
            'date':forms.DateInput(attrs={'class':'form-control','type':'date'}), 
            }
    
