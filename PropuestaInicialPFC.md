# **Propuesta para el PFC DAW-Dual**

## **Autor: Adrián García Bouzas**

## **Idea inicial**  
<p style="text-align:justify;">Se trataría de construir un portal web de gestión de activos y análisis de vulnerabilidades que permite a las empresas conocer el estado de seguridad de su infraestructura digital de forma automatizada.  </p>

<p style="text-align:justify;">Un activo se define como cualquier recurso tecnológico dentro de una organización que puede verse afectado por vulnerabilidades, como servidores, aplicaciones, bases de datos, dispositivos de red y sistemas operativos. Una de las mayores dificultades en ciberseguridad es identificar qué vulnerabilidades afectan a qué activos, lo que suele requerir procesos manuales lentos y propensos a errores.</p>  

<p style="text-align:justify;">Nuestro sistema soluciona este problema mediante el cruce de información entre los activos registrados y las vulnerabilidades CVE reportadas diariamente en fuentes oficiales como <strong>NIST (National Institute of Standards and Technology)</strong> y otras bases de datos reconocidas.  </p>

#### **¿Qué ofrecería la plataforma?**  
- **Registro y gestión de activos** para evaluar su exposición a vulnerabilidades.  
- **Cruce automático de información** entre activos y CVEs actualizados diariamente.  
- **Notificaciones y alertas** en tiempo real cuando se detectan vulnerabilidades críticas.  
- **Generación de informes personalizados** para mejorar la toma de decisiones en ciberseguridad.  

<p style="text-align:justify;">Este enfoque permite que los analistas de seguridad y sus clientes tengan una visión clara y actualizada del riesgo que enfrenta su infraestructura, reduciendo tiempos de reacción y optimizando la seguridad operativa. </p> 

## **¿Qué problema resuelve?**  
<p style="text-align:justify;">Las empresas necesitan conocer las vulnerabilidades que afectan su infraestructura tecnológica. Sin embargo, la gestión manual de CVEs es un proceso lento y propenso a errores. Los analistas de seguridad (SoC Analysts) deben revisar múltiples fuentes de información, cruzar datos con los activos de la empresa y generar informes personalizados, lo que consume tiempo crítico en un entorno de amenazas dinámicas. </p>
<p style="text-align:justify;">Nuestro sistema automatiza este proceso, detectando y notificando vulnerabilidades críticas en tiempo real, lo que optimiza la seguridad empresarial. </p> 

## **¿Por qué ahora?**  
- <p style="text-align:justify;"><strong>El número de vulnerabilidades CVE está en aumento</strong>: En los últimos 2 años se reportaron alrededor de 50.000 nuevas vulnerabilidades, lo que dificulta su gestión manual.  </p>
- <p style="text-align:justify;"><strong>Las empresas buscan soluciones eficientes</strong>: Las regulaciones de ciberseguridad exigen procesos de monitoreo y reporte más estrictos (ISO 27001, NIST, etc.).  </p>
- <p style="text-align:justify;"><strong>La automatización de procesos y Machine Learning</strong> son herramientas en auge en el campo de la ciberseguridad, ya que reducen la carga operativa y mejoran la detección proactiva.  </p>

## **¿Cómo funciona?**  

### **1. Gestión de clientes y automatización de alertas**  
<p style="text-align:justify;">Nuestra plataforma permite a las empresas registrar y gestionar sus activos tecnológicos (servidores, aplicaciones, dispositivos de red, etc.), almacenando información clave para evaluar su exposición a vulnerabilidades.  </p>

El sistema cuenta con tres roles de usuario:  
- <p style="text-align:justify;"><strong>Admin:</strong> Tiene control total sobre la plataforma, incluyendo gestión de usuarios y configuración global.  </p>
- <p style="text-align:justify;"><strong>SoC Analyst:</strong> Puede administrar los activos de los clientes a los que está asignado, generar informes personalizados y analizar vulnerabilidades.  </p>
- <p style="text-align:justify;"><strong>Cliente:</strong> Puede visualizar sus activos, las vulnerabilidades asociadas y descargar informes generados automáticamente o por un analista.  </p>

<p style="text-align:justify;">El sistema genera alertas automáticas para vulnerabilidades críticas, permitiendo a los SoC Analysts actuar de inmediato y tomar las medidas necesarias para mitigar riesgos.  </p>

### **2. Generación de informes basada en datos CVE**  
<p style="text-align:justify;">La plataforma recopila y almacena diariamente información sobre vulnerabilidades desde fuentes oficiales:</p>
 
- Extrae y actualiza los datos de vulnerabilidades, almacenándolos en nuestra base de datos.  
- Permite realizar búsquedas y correlaciones con los activos de cada cliente.  
- <p style="text-align:justify;">Genera informes automatizados con un análisis detallado del impacto de las nuevas vulnerabilidades sobre los activos registrados.  </p>
- <p style="text-align:justify;">Facilita la elaboración de reportes personalizados por parte de los SoC Analysts para clientes específicos.  </p>

