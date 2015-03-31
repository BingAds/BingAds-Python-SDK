"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class BingAdsPasswordAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=254,
                               label=_("UserName"),
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'UserName'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

    environments=(('production','Production'),
                  ('sandbox','Sandbox'))

    environment = forms.ChoiceField(label=None, required=True, choices=environments, initial=('production'))

