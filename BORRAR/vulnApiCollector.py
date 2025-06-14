import nistCollector as collector
import pandas as pd

class vulnApiCollector:

    def __init__(self, daysBack=1):
        # Constructor de la clase
        self.cve_df = pd.DataFrame(columns=["CVE","Score","Criticidad","Descripcion","Fecha Publicacion","Ultima Modificación","Url","Referencias"])
        self.cve_collector = collector.nistCollector(self.cve_df, daysBack=daysBack)

    def build_cve_dataframe(self):
        self.cve_df = self.cve_collector.search_vulnerabilities()
    
    def get_cve_dataframe(self,keywords=None):
        return self.cve_df if keywords is None else self.keyword_filter(keywords)
    
    def keyword_filter(self,keywords):
        # Filtrar por palabras clave
        return self.cve_df[self.cve_df['Descripcion'].str.contains('|'.join(keywords), case=False, na=False)]
    
    def df_is_empty(self):
        return self.cve_df.empty
    
    
