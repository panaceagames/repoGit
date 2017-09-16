# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import userProfile, _TipoCuenta, _empresas

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

class editUserForm(forms.ModelForm):
    class Meta:
        model = userProfile
        exclude = {'user','password','is_staff','is_active','is_superuser','last_login','date_joined','groups','user_permissions','verbose_name','creacion'}

class editUserFormIndividuales(forms.ModelForm):
    class Meta:
        model = userProfile
        exclude = {'user','password','is_staff','is_active','is_superuser',
            'last_login','date_joined','groups','user_permissions',
            'verbose_name','creacion', 'Tipo_Cuenta', 'Abonos', 'Empresa', 'Asociado_A_Cuenta'}


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30, label="Nombre de Usuario",widget=forms.TextInput())
    email    = forms.EmailField(label="Correo Electronico",widget=forms.TextInput())
    password_one = forms.CharField(label="Password",widget=forms.PasswordInput(render_value=False))
    password_two = forms.CharField(label="Confirmar Password",widget=forms.PasswordInput(render_value=False))
    Empresa = forms.ModelChoiceField(required=True, queryset=_empresas.objects.all())
    Rubro = forms.CharField(label="Tipo de Actividad Comercial",widget=forms.TextInput(), required=False)
    Email_Alternativo_de_Contacto = forms.EmailField(label="Correo Electronico Alternativo",widget=forms.TextInput(), required=False)
    Direccion = forms.CharField(widget=forms.TextInput(), required=False)
    Telefono = forms.CharField(widget=forms.TextInput())
    Telefono_Contacto = forms.CharField(widget=forms.TextInput(), required=False)
    Nombre_Contacto = forms.CharField(label="Nombre del Contacto",widget=forms.TextInput(), required=False)
    Abonos = forms.CharField(widget=forms.TextInput(), required=False)
    Descripcion_corta = forms.CharField(widget=forms.Textarea(), required=False)
    Asociado_A_Cuenta = forms.CharField(widget=forms.TextInput(), required=False)
    Tipo_Cuenta = forms.ChoiceField(choices=_TipoCuenta)


    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Nombre de usuario ya existe')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email ya Registrado')

    def clean_password_two(self):
        password_one = self.cleaned_data['password_one']
        password_two = self.cleaned_data['password_two']
        if password_one == password_two:
            pass
        else:
            raise forms.ValidationError('Password no coincide')

class RegisterFormTarget(forms.Form):
    username = forms.CharField(label="Nombre de Usuario",widget=forms.TextInput())
    email    = forms.EmailField(label="Correo Electronico",widget=forms.TextInput())
    password_one = forms.CharField(label="Password",widget=forms.PasswordInput(render_value=False))
    password_two = forms.CharField(label="Confirmar Password",widget=forms.PasswordInput(render_value=False))
    Rubro = forms.CharField(label="Tipo de Actividad Comercial",widget=forms.TextInput(), required=False)
    Email_Alternativo_de_Contacto = forms.EmailField(label="Correo Electronico Alternativo",widget=forms.TextInput(), required=False)
    Direccion = forms.CharField(widget=forms.TextInput(), required=False)
    Telefono = forms.CharField(widget=forms.TextInput())
    Telefono_Contacto = forms.CharField(widget=forms.TextInput(), required=False)
    Nombre_Contacto = forms.CharField(label="Nombre del Contacto",widget=forms.TextInput(), required=False)
    Descripcion_corta = forms.CharField(widget=forms.Textarea(), required=False)


    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Nombre de usuario ya existe')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email ya Registrado')

    def clean_password_two(self):
        password_one = self.cleaned_data['password_one']
        password_two = self.cleaned_data['password_two']
        if password_one == password_two:
            pass
        else:
            raise forms.ValidationError('Password no coincide')


class PasswordReset(forms.Form):
    password_one = forms.CharField(label="Password",widget=forms.PasswordInput(render_value=False))
    password_two = forms.CharField(label="Confirmar Password",widget=forms.PasswordInput(render_value=False))

    def clean_password_two(self):
        password_one = self.cleaned_data['password_one']
        password_two = self.cleaned_data['password_two']
        if password_one == password_two:
            pass
        else:
            raise forms.ValidationError('Password no coincide')

class FormEmpresas(forms.ModelForm):
    class Meta:
        model = _empresas
        exclude = {}