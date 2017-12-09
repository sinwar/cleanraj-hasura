from django import forms
import re
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from account.conf import settings
from account.hooks import hookset
from account.utils import get_user_lookup_kwargs
from django.utils.translation import ugettext_lazy as _
from . import models
import account.forms

alnum_re = re.compile(r"^\w+$")

# Integrated sign up form from account app
class SignupForm(account.forms.SignupForm):

    first_name = forms.CharField(
        label = _("First Name"),
        max_length = 30,
        required = True
    )
    last_name = forms.CharField(
        label =_("Last Name"),
        max_length = 30,
        required = True
    )

    # validator for first name
    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not alnum_re.search(first_name):
            raise forms.ValidationError(_("First name can only contain letters, numbers and underscores."))

        return first_name

    # validator for last name
    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not alnum_re.search(last_name):
            raise forms.ValidationError(_("Last name can only contain letters, numbers and underscores."))

        return last_name
