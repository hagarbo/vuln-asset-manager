import requests
from datetime import datetime,timedelta
import pandas as pd
import time
from Util import logger, get_date_from_timezonedate

class nistCollector:
    def __init__(self,df_template, daysBack=1, resultsPerPage=1000):
        self.endDate = datetime.now()
        self.startDate = self.endDate - timedelta(days=daysBack) # Maximo 120 dias consecutivos
        self.resultsPerPage = resultsPerPage
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.api_key = "22b648dd-54b7-4864-bcdf-c25039201472"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.cve_df = df_template

    # Función para realizar la solicitud y obtener vulnerabilidades
    def build_dataframe(self,offset=0):
        # Definir los parámetros comunes de búsqueda
        params = {
                "lastModStartDate": self.startDate.isoformat(),  # Fecha de inicio
                "lastModEndDate": self.endDate.isoformat(),      # Fecha de fin
                "resultsPerPage": self.resultsPerPage,           # Número de resultados por página
                "startIndex": offset                             # Página de resultados
            }
        # Realizar la solicitud a la API
        response = self.send_api_request(params)
                   
        if response.status_code == 200:
            data = response.json()  # Convertir la respuesta JSON a un diccionario de Python
            # Verificar si hay resultados
            if data['totalResults']>0:
                self.process_response(data)
                if data['totalResults']>(offset+self.resultsPerPage):self.build_dataframe(offset=offset+self.resultsPerPage)
            else:
                logger.info(f"No se encontraron vulnerabilidades en las fechas seleccionadas")
        else:
            logger.info(f"Error en la solicitud: {response.status_code}")
        
    def send_api_request(self,params):
        error_503_403 = True
        retrys = 10

        while error_503_403 and retrys !=0:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            logger.info("Realizada la peticion:",response.request.url)
            if response.status_code != 503 and response.status_code != 403:
                error_503_403 = False
            elif response.status_code == 403:
                retrys-=1
                logger.info(f"Error 503: Esperamos 10 segundos y reintentamos. Intentos restantes: {retrys}") 
                time.sleep(10)  
            else:
                retrys-=1
                logger.info(f"Error 503: Esperamos 10 segundos y reintentamos. Intentos restantes: {retrys}") 
                time.sleep(10)
        return response

    def process_response(self,data):
        vulnerabilities = data['vulnerabilities']
        for vulnerability in vulnerabilities:
            if vulnerability['cve']['vulnStatus'] != "Rejected":
                cve_id = vulnerability['cve']['id']
                # Si hay descripcion en español tiene prioridad
                try:
                    description = vulnerability['cve']['descriptions'][1]['value']
                except Exception:
                    description = vulnerability['cve']['descriptions'][0]['value']

                published_date =  get_date_from_timezonedate(vulnerability['cve']['published'])
                last_modified_date = get_date_from_timezonedate(vulnerability['cve']['lastModified'])

                # Score
                try:
                    cvssScore = vulnerability['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']
                    cvssSeverity = vulnerability['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseSeverity']
                except Exception:
                    cvssScore = '-'
                    cvssSeverity = '-'
                
                # References
                referenceList = []
                for reference in vulnerability['cve']['references']:
                    referenceList.append(reference['url'])
                # Imprimir los detalles de cada vulnerabilidad
                logger.info(f"CVE ID: {cve_id}")

                # Añadimos al dataframe
                new_row = pd.DataFrame({"CVE":[cve_id],"Score":[cvssScore],"Criticidad":[cvssSeverity],"Descripcion":[description],"Fecha Publicacion":[published_date],"Ultima Modificación":[last_modified_date],"Url":[f"{self.base_url}/{cve_id}"],"Referencias":[referenceList]})
                self.cve_df = pd.concat([self.cve_df, new_row],ignore_index=True)
    
    def search_vulnerabilities(self):
        self.build_dataframe()
        return self.cve_df