"""
Configuración del panel de administración de Django.
Define la interfaz de administración para:
- Roles y permisos
- Reportes de Power BI
- Asignaciones de usuarios a roles
"""

from django.contrib import admin
from .models import Role, UserRole, PowerBIReport

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Roles.
    Permite gestionar roles y sus permisos asociados.
    """
    list_display = ('name', 'description', 'windows_group', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'windows_group')
    list_filter = ('created_at', 'updated_at')
    fields = ('name', 'description', 'windows_group', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para asignaciones de roles a usuarios.
    Permite gestionar qué usuarios tienen qué roles.
    """
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'role__name')

@admin.register(PowerBIReport)
class PowerBIReportAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Reportes de Power BI.
    Permite gestionar reportes y sus roles asociados.
    """
    list_display = ('name', 'report_id', 'workspace_id', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'report_id', 'workspace_id')
    list_filter = ('created_at', 'updated_at')
    filter_horizontal = ('roles',)
    ordering = ('name',)
