from django.core.management.base import BaseCommand
from powerbi_reports.pbirs_client import PBIRSClient
from reports.models import PowerBIReport
from django.conf import settings

class Command(BaseCommand):
    help = 'Importa automáticamente los reportes desde PBIRS a la base de datos de Django'

    def handle(self, *args, **kwargs):
        pbirs_conf = getattr(settings, 'PBIRS_CONFIG', {})
        pbirs_url = pbirs_conf.get('SERVER_URL', 'http://localhost/ReportServer')
        pbirs_user = pbirs_conf.get('USERNAME', '')
        pbirs_pass = pbirs_conf.get('PASSWORD', '')

        client = PBIRSClient(pbirs_url, pbirs_user, pbirs_pass)
        self.stdout.write(self.style.NOTICE('Obteniendo lista de reportes desde PBIRS...'))
        try:
            response = client.session.get(f"{pbirs_url}/api/v2.0/Reports")
            print('Respuesta cruda de la API:')
            print('Status code:', response.status_code)
            print('Headers:', response.headers)
            print('Content:', response.text)
            response.raise_for_status()
            reportes = response.json()
            nuevos = 0
            for rep in reportes.get('value', []):
                report_id = rep.get('Id') or rep.get('id') or rep.get('Path')
                name = rep.get('Name') or rep.get('name')
                description = rep.get('Description', '')
                workspace_id = rep.get('Path', '')
                if not PowerBIReport.objects.filter(report_id=report_id).exists():
                    PowerBIReport.objects.create(
                        report_id=report_id,
                        name=name,
                        description=description,
                        workspace_id=workspace_id
                    )
                    nuevos += 1
            self.stdout.write(self.style.SUCCESS(f'Importación completada. {nuevos} nuevos reportes agregados.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al importar reportes: {str(e)}')) 