from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from finance.models import Charge, Account, Goal, User
from django.forms.widgets import PasswordInput
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


class ChargeForm(ModelForm):
    class Meta:
        model = Charge
        fields = ['value', 'date', 'purpose', 'category']

    def clean_date(self):
        try:
            date = self.cleaned_data.get('date')
        except:
            raise ValidationError('Invalid data input')
        return date

    def clean_value(self):
        try:
            value = self.cleaned_data.get('value')
        except:
            raise ValidationError('Invalid money input')
        return value

    def clean(self):

        value = self.clean_value()
        date = self.clean_date()

        if (value <= 0)and(date >= date.today()):
            raise ValidationError('You can not spend money in the future')


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = ['goalValue', 'purpose', 'category']

    def clean_goalValue(self):
        try:
            goalValue = self.cleaned_data.get('goalValue')
        except:
            raise ValidationError('Invalid money input')

        print(goalValue)
        if goalValue <= 0:
            raise ValidationError('You can not make negative goal')
        return goalValue


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'total']

    def clean_name(self):
        try:
            name = self.cleaned_data.get('name')
        except:
            raise ValidationError('Invalid name input')
        return name

    def clean_total(self):
        try:
            total = self.cleaned_data.get('total')
            if total < 0:
                raise ValidationError('Invalid total input')
        except:
            raise ValidationError('Invalid total input')
        return total


class GetAccountsListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user_id')
        print(user)
        super(GetAccountsListForm, self).__init__(*args, **kwargs)
        self.fields['account'] = forms.ModelChoiceField(queryset=Account.objects.filter(user_id=user),
                                                        initial=0,
                                                        to_field_name='account_number')


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'phone_number', 'address']
        widgets = {
            'password': PasswordInput
        }

    def clean_phone_number(self):
        try:
            phone = self.cleaned_data['phone_number']
            ph = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(ph):
                raise ValidationError('Invalid phone number input')
        except NumberParseException:
            if phone == "":
                return phone
            raise ValidationError('Invalid phone number input (parse)')
        return phone


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=PasswordInput)


class AddCashToGoal(forms.Form):
    addvalue = forms.DecimalField(decimal_places=2, max_digits=8)

    def clean_addvalue(self):
        val = self.cleaned_data['addvalue']
        if val <= 0:
            raise forms.ValidationError("Value can not be zero or negative")
        return val


class EditProfile(forms.Form):
    username = forms.CharField(required=False)
    password = forms.CharField(widget=PasswordInput, required=False)
    phone_number = forms.CharField(required=False)
    address = forms.CharField(required=False)

    def clean_phone_number(self):
        try:
            phone = self.cleaned_data['phone_number']
            ph = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(ph):
                raise ValidationError('Invalid phone number input')
        except NumberParseException:
            if phone == "":
                return phone
            raise ValidationError('Invalid phone number input (parse)')
        return phone

    def clean_username(self):
        try:
            username = self.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                raise ValidationError('User with this name is already exists')
        except:
            raise ValidationError('Invalid username input')
        return username
