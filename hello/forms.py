from django import forms
from.models import Study
from.models import Profile
import datetime
from datetime import datetime as dt
now = datetime.datetime.now()
y = now.year
m = now.month

from django.contrib.auth.models import User

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ['year','month','day','hour', 'comment']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile      
        fields = ['language', 'purpose', 'weekday_study', 'holiday_study', 'is_private', 'is_continue']

class FindForm(forms.Form):
    find_year = forms.IntegerField(label='年', initial=y , required=True)
    find_month = forms.IntegerField(label='月', initial=m, required=False)

class FindYearForm(forms.Form):
    find_year = forms.IntegerField(label='年', initial=y, required=True)


class SignUpForm(forms.Form):
    username = forms.CharField(label='ニックネーム', widget=forms.TextInput)
    enter_password = forms.CharField(label='パスワードを入力', widget=forms.PasswordInput)
    retype_password = forms.CharField(label='パスワードを再入力', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('このユーザー名は既に使われています。')
        return username

    def clean_enter_password(self):
        password = self.cleaned_data.get('enter_password')
        if len(password) < 8:
            raise forms.ValidationError('パスワードは8文字以上である必要があります。')
        return password

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('enter_password')
        retyped = self.cleaned_data.get('retype_password')
        if password and retyped and (password != retyped):
            self.add_error(None, 'パスワードが違っています。')
        return self.cleaned_data

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('enter_password')
        new_user = User.objects.create_user(username = username)
        new_user.set_password(password)
        new_user.save()
