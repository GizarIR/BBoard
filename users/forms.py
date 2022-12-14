from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    AuthenticationForm as DjangoAuthenticationForm
)
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .utils import send_email_for_verify, clear_old_code
from bboard.tasks import send_email_for_verify_celery
from project.settings import USE_CELERY_SEND_EMAIL

User = get_user_model()

class EmailVerifyForm(forms.Form):
    code = forms.CharField(max_length=12, label='одноразовый код')


class MyAuthenticationForm(DjangoAuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()

            if not self.user_cache.email_verify:
                clear_old_code(self.user_cache)
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Ваш email не подтвержден, вам повторно отправлен email c кодом, '
                    'проверьте Ваш email и следуйте инструкциям',
                    code="invalid_login",
                )

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class MyUserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
