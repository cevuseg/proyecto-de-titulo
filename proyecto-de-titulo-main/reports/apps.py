"""
Configuración de la aplicación de reportes.
Define la configuración básica de la aplicación Django para el sistema de reportes.
"""

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """
    Configuración de la aplicación de reportes.
    Define el nombre y la configuración inicial de la aplicación.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
    verbose_name = 'Sistema de Reportes Power BI'

    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está lista.
        Aquí se pueden realizar configuraciones adicionales o
        registrar señales si es necesario.
        """
        pass
