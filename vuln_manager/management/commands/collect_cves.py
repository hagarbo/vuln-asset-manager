from django.core.management.base import BaseCommand
from vuln_manager.services.cve.nist_cve_collector import NISTCVECollector
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository

class Command(BaseCommand):
    help = 'Recolecta CVEs desde NIST y las almacena en la base de datos.'

    def handle(self, *args, **options):
        collector = NISTCVECollector(days_back=1)
        cves = collector.fetch_cves()
        repo = VulnerabilidadRepository()
        nuevas, actualizadas = 0, 0
        for dto in cves:
            _, created = repo.create_or_update_from_dto(dto)
            if created:
                nuevas += 1
            else:
                actualizadas += 1
        self.stdout.write(self.style.SUCCESS(f'Se han procesado {len(cves)} CVEs ({nuevas} nuevas, {actualizadas} actualizadas).')) 