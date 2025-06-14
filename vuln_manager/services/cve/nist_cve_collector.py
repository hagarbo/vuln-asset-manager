import requests
from datetime import datetime, timedelta
from typing import List
from .dto import VulnerabilidadDTO

class NISTCVECollector:
    BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    API_KEY = "22b648dd-54b7-4864-bcdf-c25039201472"  # Considera moverlo a settings o variable de entorno
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}
    RESULTS_PER_PAGE = 1000

    def __init__(self, days_back=1):
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=days_back)

    def fetch_cves(self) -> List[VulnerabilidadDTO]:
        cves = []
        offset = 0
        total_results = 1  # Inicializar para entrar en el bucle
        while offset < total_results:
            params = {
                "lastModStartDate": self.start_date.isoformat(),
                "lastModEndDate": self.end_date.isoformat(),
                "resultsPerPage": self.RESULTS_PER_PAGE,
                "startIndex": offset
            }
            response = self._send_api_request(params)
            if response.status_code == 200:
                data = response.json()
                total_results = data.get('totalResults', 0)
                cves.extend(self._process_response(data))
                offset += self.RESULTS_PER_PAGE
            else:
                break
        return cves

    def _send_api_request(self, params):
        error_503_403 = True
        retrys = 10
        while error_503_403 and retrys != 0:
            response = requests.get(self.BASE_URL, params=params, headers=self.HEADERS)
            if response.status_code not in (503, 403):
                error_503_403 = False
            else:
                retrys -= 1
                import time; time.sleep(10)
        return response

    def _process_response(self, data) -> List[VulnerabilidadDTO]:
        cve_list = []
        for item in data.get('vulnerabilities', []):
            cve = item['cve']
            if cve.get('vulnStatus') == "Rejected":
                continue
            cve_id = cve.get('id')
            # Descripciones
            descripcion_en = ''
            descripcion_es = ''
            for desc in cve.get('descriptions', []):
                if desc.get('lang') == 'es':
                    descripcion_es = desc.get('value', '')
                elif desc.get('lang') == 'en':
                    descripcion_en = desc.get('value', '')
            # Fechas
            fecha_publicacion = cve.get('published', '')
            fecha_modificacion = cve.get('lastModified', '')
            # Status
            status = cve.get('vulnStatus', 'published')
            
            # Procesar datos de CVSS de forma dinámica
            cvss_data = {}
            severidad = 'no_establecida'
            
            if 'metrics' in cve:
                for metric_key, metric_value in cve['metrics'].items():
                    if metric_value and isinstance(metric_value, list) and len(metric_value) > 0:
                        cvss_info = metric_value[0].get('cvssData', {})
                        if cvss_info:
                            version = cvss_info.get('version', '')
                            if version:
                                cvss_data[version] = {
                                    'score': cvss_info.get('baseScore'),
                                    'severidad': cvss_info.get('baseSeverity'),
                                    'vector': cvss_info.get('vectorString')
                                }
                                # Usar la severidad de la versión más reciente de CVSS
                                if version.startswith('3.') or version.startswith('4.'):
                                    severidad = cvss_info.get('baseSeverity', 'no establecida').lower()
            
            # Referencias
            referencias = [ref['url'] for ref in cve.get('references', [])]
            
            cve_list.append(VulnerabilidadDTO(
                cve_id=cve_id,
                descripcion_en=descripcion_en,
                descripcion_es=descripcion_es,
                severidad=severidad,
                status=status,
                fecha_publicacion=fecha_publicacion,
                fecha_modificacion=fecha_modificacion,
                cvss_data=cvss_data,
                referencias=referencias
            ))
        return cve_list 