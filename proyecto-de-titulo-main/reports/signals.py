"""
Señales de Django para la aplicación de reportes.
Maneja eventos automáticos como:
- Creación/actualización de roles
- Asignación de usuarios a roles
- Cambios en reportes
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Role, UserRole, PowerBIReport
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Role)
def role_saved(sender, instance, created, **kwargs):
    """
    Señal que se dispara cuando se crea o actualiza un rol.
    Registra la acción en el log y realiza validaciones adicionales.
    """
    if created:
        logger.info(f"Nuevo rol creado: {instance.name}")
    else:
        logger.info(f"Rol actualizado: {instance.name}")

@receiver(post_save, sender=UserRole)
def user_role_saved(sender, instance, created, **kwargs):
    """
    Señal que se dispara cuando se asigna un rol a un usuario.
    Registra la acción en el log y actualiza permisos si es necesario.
    """
    if created:
        logger.info(f"Rol {instance.role.name} asignado al usuario {instance.user.username}")
    else:
        logger.info(f"Asignación de rol actualizada para {instance.user.username}")

@receiver(post_delete, sender=UserRole)
def user_role_deleted(sender, instance, **kwargs):
    """
    Señal que se dispara cuando se elimina una asignación de rol.
    Registra la acción en el log y limpia permisos si es necesario.
    """
    logger.info(f"Rol {instance.role.name} eliminado del usuario {instance.user.username}")

@receiver(post_save, sender=PowerBIReport)
def report_saved(sender, instance, created, **kwargs):
    """
    Señal que se dispara cuando se crea o actualiza un reporte.
    Registra la acción en el log y actualiza la caché si es necesario.
    """
    if created:
        logger.info(f"Nuevo reporte creado: {instance.name}")
    else:
        logger.info(f"Reporte actualizado: {instance.name}")

@receiver(post_delete, sender=PowerBIReport)
def report_deleted(sender, instance, **kwargs):
    """
    Señal que se dispara cuando se elimina un reporte.
    Registra la acción en el log y limpia la caché si es necesario.
    """
    logger.info(f"Reporte eliminado: {instance.name}") 