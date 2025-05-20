"""
Pruebas unitarias y de integración para la aplicación de reportes.
Incluye pruebas para:
- Modelos (Roles, Reportes, Asignaciones)
- Vistas (Dashboard, Visualización de reportes)
- Integración con PBIRS
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Role, UserRole, PowerBIReport
from powerbi_reports.pbirs_client import PBIRSClient
import unittest
from unittest.mock import patch, MagicMock

class RoleModelTest(TestCase):
    """
    Pruebas para el modelo Role.
    Verifica la creación y validación de roles.
    """
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.role = Role.objects.create(
            name="Test Role",
            description="Role for testing",
            windows_group="TEST_GROUP"
        )

    def test_role_creation(self):
        """Verifica la creación correcta de un rol."""
        self.assertEqual(self.role.name, "Test Role")
        self.assertEqual(self.role.description, "Role for testing")
        self.assertEqual(self.role.windows_group, "TEST_GROUP")

class PowerBIReportTest(TestCase):
    """
    Pruebas para el modelo PowerBIReport.
    Verifica la creación y validación de reportes.
    """
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.report = PowerBIReport.objects.create(
            name="Test Report",
            report_id="123",
            description="Test Description",
            workspace_id="workspace1",
            path="/reports/test"
        )

    def test_report_creation(self):
        """Verifica la creación correcta de un reporte."""
        self.assertEqual(self.report.name, "Test Report")
        self.assertEqual(self.report.report_id, "123")
        self.assertEqual(self.report.workspace_id, "workspace1")

class ViewTests(TestCase):
    """
    Pruebas para las vistas de la aplicación.
    Verifica el comportamiento de las vistas principales.
    """
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.role = Role.objects.create(name="Test Role")
        self.user_role = UserRole.objects.create(
            user=self.user,
            role=self.role
        )

    def test_dashboard_access(self):
        """Verifica el acceso al dashboard."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(response.status_code, 200)

    @patch('powerbi_reports.pbirs_client.PBIRSClient')
    def test_view_report(self, mock_pbirs):
        """Verifica la visualización de un reporte."""
        # Configurar el mock de PBIRS
        mock_pbirs.return_value.check_permissions.return_value = True
        
        self.client.login(username='testuser', password='testpass123')
        report = PowerBIReport.objects.create(
            name="Test Report",
            report_id="123",
            roles=[self.role]
        )
        
        response = self.client.get(
            reverse('reports:view_report', args=[report.report_id])
        )
        self.assertEqual(response.status_code, 302)  # Redirección a PBIRS

class PBIRSIntegrationTest(TestCase):
    """
    Pruebas de integración con Power BI Report Server.
    Verifica la comunicación con el servidor de reportes.
    """
    @patch('powerbi_reports.pbirs_client.PBIRSClient')
    def test_report_sync(self, mock_pbirs):
        """Verifica la sincronización de reportes con PBIRS."""
        # Configurar el mock de PBIRS
        mock_pbirs.return_value.get_reports.return_value = [
            {
                'Id': '123',
                'Name': 'Test Report',
                'Description': 'Test Description',
                'Path': '/reports/test'
            }
        ]
        
        client = Client()
        user = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        client.login(username='admin', password='admin123')
        
        response = client.get(reverse('reports:sync_reports'))
        self.assertEqual(response.status_code, 302)  # Redirección después de sincronizar
        
        # Verificar que el reporte se creó en la base de datos
        self.assertTrue(
            PowerBIReport.objects.filter(report_id='123').exists()
        )
