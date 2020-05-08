from django import forms
from .models import MyUser
from django.core.exceptions import ValidationError
from .models import MyUser,Tweet,Comment
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class ContactForm(forms.Form):
    name = forms.CharField( max_length=250,)
    email = forms.EmailField(label='Email',)
    category = forms.ChoiceField(choices=[('question','Question'),( 'other','Other')],)
    subject = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea)



class MyUserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input is-success'}))
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'input is-success'}))

    class Meta:
        model = MyUser
        fields = ('email','favorite_color','user_type',)
        
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input', 'required': True}),
            'favorite_color': forms.TextInput(attrs={'class': 'input', 'autofocus': True}),
            'user_type':forms.Select(attrs={'class': 'select is-primary is-fullwidth',}),
            'password' : forms.PasswordInput(attrs={'class': 'input is-success'}),
        }

class MyUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ('email','favorite_color','user_type',)
        
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input', 'required': True}),
            'favorite_color': forms.TextInput(attrs={'class': 'input', 'autofocus': True}),
            'user_type':forms.Select(attrs={'class': 'select is-primary is-fullwidth',}),
            'password' : forms.PasswordInput(attrs={'class': 'input is-success'}),
        }


# class RegisterForm(forms.ModelForm):
# class RegisterForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input is-success'}))
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'input is-success'}))

#     class Meta:
#         model = MyUser
#         fields = ('email','favorite_color','user_type',)
        
#         widgets = {
#             'email': forms.EmailInput(attrs={'class': 'input', 'required': True}),
#             'favorite_color': forms.TextInput(attrs={'class': 'input', 'autofocus': True}),
#             'user_type':forms.Select(attrs={'class': 'select is-primary is-fullwidth',})
#         }

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
    
#         if commit:
#             user.save()
#         return user

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Save person',css_class='btn-success'))


# class LoginForm(forms.Form):
#     email = forms.EmailField(label='Email',widget =forms.EmailInput(attrs={'class': 'input'}))
#     password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input is-success'}))

# class LoginForm(forms.ModelForm):
    
#     class Meta:
#         model = MyUser
#         fields = ("email","password")


class MyUserForm(forms.ModelForm):
    
    class Meta:
        model = MyUser
        fields = ('email','password','favorite_color','user_type')


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["text"]
        widgets = {
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
        }

class ReviewForm(forms.Form):
    new_comment = forms.CharField(max_length=300,
    widget=forms.Textarea(attrs={'cols': 50, 'rows': 6}),
    required=False)
    APPROVAL_CHOICES = (
        ('approve', 'Approve this tweet and post it to Twitter'),
        ('reject','Reject this tweet and send it back to the author with your comment'),
    )
    approval = forms.ChoiceField(choices=APPROVAL_CHOICES, widget=forms.RadioSelect)

