from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['service', 'login', 'password', 'url', 'notes']
        widgets = {
            # EncryptedField наследуется от TextField, ModelForm по умолчанию
            # рендерил бы его как <textarea> — явно указываем PasswordInput,
            # раз уж где-то этот form когда-нибудь будет рендериться через {{ form.password }}.
            'password': forms.PasswordInput(),
        }
