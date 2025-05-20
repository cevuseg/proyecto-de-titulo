"""
Modelos de datos para el sistema de reportes Power BI.
Este módulo define la estructura de datos para:
- Roles y permisos de usuarios
- Reportes de Power BI
- Registro de accesos
- Relaciones entre entidades
"""

from django.db import models
from django.contrib.auth.models import User

# reports/models.py: Define los modelos de datos principales del sistema.
# Incluye roles, usuarios, reportes, permisos, logs, etc.

# Create your models here.

class Role(models.Model):
    """
    Modelo para gestionar los roles de usuario en el sistema.
    Cada rol puede tener múltiples usuarios y múltiples reportes asociados.
    También se mapea a grupos de Windows/AD para control de acceso.
    """
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Nombre",
        help_text="Nombre único del rol (ej: Administrador, Usuario)"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Descripción",
        help_text="Descripción detallada del rol y sus permisos"
    )
    windows_group = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Grupo/Usuario Windows/AD",
        help_text="Grupo o usuario de Windows/AD asociado (ej: DESKTOP-M5D5K4J\\Finanzas)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última actualización"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['name']

class UserRole(models.Model):
    """
    Modelo para asignar roles a usuarios.
    Establece una relación muchos a muchos entre usuarios y roles.
    Permite que un usuario tenga múltiples roles y viceversa.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Usuario",
        help_text="Usuario al que se asigna el rol"
    )
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE, 
        verbose_name="Rol",
        help_text="Rol asignado al usuario"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de asignación"
    )

    class Meta:
        unique_together = ('user', 'role')
        verbose_name = "Rol de Usuario"
        verbose_name_plural = "Roles de Usuario"

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

class PowerBIReport(models.Model):
    """
    Modelo para gestionar los reportes de Power BI.
    Cada reporte puede estar asociado a múltiples roles.
    Almacena la información necesaria para acceder y mostrar los reportes.
    """
    report_id = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="ID del Reporte",
        help_text="Identificador único del reporte en Power BI"
    )
    name = models.CharField(
        max_length=200, 
        verbose_name="Nombre",
        help_text="Nombre descriptivo del reporte"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Descripción",
        help_text="Descripción detallada del reporte"
    )
    workspace_id = models.CharField(
        max_length=100, 
        verbose_name="ID del Espacio de Trabajo",
        help_text="Identificador del workspace en Power BI"
    )
    path = models.CharField(
        max_length=500,
        verbose_name="Ruta del Reporte",
        help_text="Ruta completa del reporte en PBIRS (ej: /Carpeta/Subcarpeta/Reporte)",
        blank=True,
        default=''
    )
    roles = models.ManyToManyField(
        Role, 
        related_name='reports', 
        verbose_name="Roles con acceso",
        help_text="Roles que tienen permiso para ver este reporte"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última actualización"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Reporte de Power BI"
        verbose_name_plural = "Reportes de Power BI"
        ordering = ['name']

    def get_absolute_url(self):
        """
        Retorna la URL completa del reporte en PBIRS.
        Esta URL se usa para mostrar el reporte en el visor.
        """
        from django.conf import settings
        pbirs_url = settings.PBIRS_CONFIG.get('REPORT_MANAGER_URL', 'http://localhost/Reports')
        return f"{pbirs_url}/Pages/ReportViewer.aspx?%2f{self.path.lstrip('/')}"
