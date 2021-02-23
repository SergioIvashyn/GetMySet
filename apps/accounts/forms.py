from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    PasswordResetForm,
    AuthenticationForm,
)
from django.conf import settings
from .models import User


class UserChangeForm(BaseUserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ),
    )

    class Meta:
        model = User
        fields = forms.ALL_FIELDS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password(self):
        return self.initial['password']


class UserCreationForm(BaseUserCreationForm):
    """
    A form that creates a user, with no privileges,
    from the given email, phone and password.
    """
    error_messages = {
        'duplicate_email': _("This email address is already registered by another user."),
        'password_mismatch': _("The two passwords you filled out do not match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Please re-enter your password for verification purposes."),
    )

    class Meta:
        model = User
        fields = forms.ALL_FIELDS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'name',
            'email',
        )

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.is_email_changed = False

    def set_is_email_changed(self, value: bool) -> None:
        self.is_email_changed = value

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.email == email:
            return email
        else:
            uu = User.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
            if uu:
                raise forms.ValidationError(_('This email address is already using by another user.'))
            self.set_is_email_changed(True)
        return email

    def save(self, *args, **kwargs):
        instance: User = super(EditUserForm, self).save(*args, **kwargs)
        if self.is_email_changed:
            instance.deactivate()


class UserRegistrationForm(UserCreationForm):
    invite_code = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ('email', 'name')


class UserPasswordSetupForm(forms.Form):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Please re-enter your password for verification purposes."),
    )

    error_messages = {
        'password_mismatch': _("The two passwords you filled out do not match."),
    }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2


class UserAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            'Please enter correct email address and password. '
            'Note that both fields are case-sensitive.'
        ),
        'inactive': _('This account is inactive.'),
    }

    def __init__(self, request=None, *args, **kwargs):
        super(UserAuthForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].label = _('Email')
        self.fields['username'].widget = forms.EmailInput()


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name',)


class EditUserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
