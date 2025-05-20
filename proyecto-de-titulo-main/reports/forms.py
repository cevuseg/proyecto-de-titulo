"""
Formularios para la aplicación de reportes.
Define los formularios para:
- Gestión de roles
- Asignación de usuarios a roles
- Configuración de reportes
"""

from django import forms
from django.contrib.auth.models import User
from .models import Role, UserRole, PowerBIReport

class RoleForm(forms.ModelForm):
    """
    Formulario para crear y editar roles.
    Permite definir el nombre, descripción y grupo de Windows asociado.
    """
    class Meta:
        model = Role
        fields = ['name', 'description', 'windows_group']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'windows_group': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserRoleForm(forms.ModelForm):
    """
    Formulario para asignar roles a usuarios.
    Permite seleccionar un usuario y un rol para crear la asignación.
    """
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserRole
        fields = ['user', 'role']

class PowerBIReportForm(forms.ModelForm):
    """
    Formulario para crear y editar reportes de Power BI.
    Permite definir la información básica del reporte y sus roles asociados.
    """
    class Meta:
        model = PowerBIReport
        fields = ['name', 'description', 'report_id', 'workspace_id', 'path', 'roles']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'report_id': forms.TextInput(attrs={'class': 'form-control'}),
            'workspace_id': forms.TextInput(attrs={'class': 'form-control'}),
            'path': forms.TextInput(attrs={'class': 'form-control'}),
            'roles': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class ReportSearchForm(forms.Form):
    """
    Formulario de búsqueda de reportes.
    Permite filtrar reportes por nombre, descripción o rol.
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar reportes...'
        })
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    ) 