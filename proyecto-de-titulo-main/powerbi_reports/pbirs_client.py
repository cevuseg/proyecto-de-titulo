"""
Cliente para interactuar con Power BI Report Server (PBIRS).
Este módulo proporciona una interfaz para:
- Autenticación con PBIRS
- Obtención de reportes
- Gestión de permisos
- Visualización de reportes
"""

import requests
from requests_ntlm import HttpNtlmAuth
from zeep import Client
from zeep.transports import Transport
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class PBIRSClient:
    """
    Cliente para interactuar con Power BI Report Server.
    Maneja la autenticación y las operaciones con el servidor de reportes.
    """

    def __init__(self, server_url=None, username=None, password=None):
        """
        Inicializa el cliente PBIRS.
        
        Args:
            server_url (str): URL del servidor de reportes
            username (str): Usuario para autenticación
            password (str): Contraseña para autenticación
        """
        self.server_url = server_url or settings.PBIRS_CONFIG['SERVER_URL']
        self.username = username or settings.PBIRS_CONFIG['USERNAME']
        self.password = password or settings.PBIRS_CONFIG['PASSWORD']
        self.session = requests.Session()
        self.session.auth = HttpNtlmAuth(self.username, self.password)
        self.session.verify = settings.PBIRS_CONFIG.get('VERIFY_SSL', False)

    def get_reports(self):
        """
        Obtiene la lista de reportes disponibles.
        
        Returns:
            list: Lista de reportes disponibles
        """
        try:
            response = self.session.get(f"{self.server_url}/api/v2.0/Reports")
            response.raise_for_status()
            return response.json().get('value', [])
        except Exception as e:
            logger.error(f"Error al obtener reportes: {e}")
            return []

    def get_report_by_id(self, report_id):
        """
        Obtiene un reporte específico por su ID.
        
        Args:
            report_id (str): ID del reporte
            
        Returns:
            dict: Información del reporte
        """
        try:
            response = self.session.get(f"{self.server_url}/api/v2.0/Reports({report_id})")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error al obtener reporte {report_id}: {e}")
            return None

    def get_report_content(self, report_id):
        """
        Obtiene el contenido de un reporte.
        
        Args:
            report_id (str): ID del reporte
            
        Returns:
            bytes: Contenido del reporte
        """
        try:
            response = self.session.get(
                f"{self.server_url}/api/v2.0/Reports({report_id})/Content",
                stream=True
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error al obtener contenido del reporte {report_id}: {e}")
            return None

    def check_permissions(self, report_id, username):
        """
        Verifica los permisos de un usuario para un reporte.
        
        Args:
            report_id (str): ID del reporte
            username (str): Nombre de usuario
            
        Returns:
            bool: True si el usuario tiene permisos
        """
        try:
            response = self.session.get(
                f"{self.server_url}/api/v2.0/Reports({report_id})/Permissions",
                params={'username': username}
            )
            response.raise_for_status()
            return response.json().get('hasAccess', False)
        except Exception as e:
            logger.error(f"Error al verificar permisos para {username} en reporte {report_id}: {e}")
            return False

    def get_report_list(self):
        """Obtiene la lista de reportes disponibles en el servidor."""
        try:
            response = self.session.get(f"{self.server_url}/Reports/api/v2.0/Reports")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error al obtener la lista de reportes: {str(e)}")
            raise

    def get_report_parameters(self, report_path):
        """Obtiene los parámetros de un reporte específico."""
        try:
            response = self.session.get(
                f"{self.server_url}/Reports/api/v2.0/Reports(Path='{report_path}')/Parameters"
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error al obtener parámetros del reporte: {str(e)}")
            raise

    def get_report_metadata(self, report_path):
        """Obtiene los metadatos de un reporte específico."""
        try:
            response = self.session.get(
                f"{self.server_url}/Reports/api/v2.0/Reports(Path='{report_path}')"
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error al obtener metadatos del reporte: {str(e)}")
            raise

    def get_access_token(self):
        """
        Obtiene un token de acceso para incrustar reportes.
        En PBIRS, esto generalmente implica obtener un token de autenticación.
        """
        try:
            # Obtener el token de autenticación de la sesión actual
            response = self.session.get(f"{self.server_url}/Reports/api/v2.0/Reports")
            response.raise_for_status()
            
            # Extraer el token de las cookies o headers de la respuesta
            # Esto puede variar según la configuración de tu PBIRS
            token = response.cookies.get('ReportServerAuth') or response.headers.get('X-Auth-Token')
            
            if not token:
                raise Exception("No se pudo obtener el token de acceso")
                
            return token
            
        except Exception as e:
            logger.error(f"Error al obtener token de acceso: {str(e)}")
            raise 