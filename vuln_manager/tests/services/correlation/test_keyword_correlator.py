import pytest
from vuln_manager.services.correlation.keyword_correlator import KeywordCorrelator
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from vuln_manager.models.activo_vulnerabilidad.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.models.cliente.cliente import Cliente
from vuln_manager.models.auth.usuario import Usuario

@pytest.fixture(autouse=True)
def limpiar_tablas(db):
    ActivoVulnerabilidad.objects.all().delete()
    Alerta.objects.all().delete()
    yield
    ActivoVulnerabilidad.objects.all().delete()
    Alerta.objects.all().delete()

@pytest.fixture
def usuario_cliente_fixture(db):
    return Usuario.objects.create_user(username='cliente_demo', password='demo', rol='cliente')

@pytest.fixture
def cliente_fixture(db, usuario_cliente_fixture):
    return Cliente.objects.create(nombre='Cliente Demo', usuario=usuario_cliente_fixture)

@pytest.fixture
def activos_fixture(db, cliente_fixture):
    # Crear activos de ejemplo con palabras clave
    activos = [
        Activo.objects.create(nombre='Servidor Web', tipo='hardware', palabras_clave='apache,nginx,web', cliente=cliente_fixture),
        Activo.objects.create(nombre='Base de Datos', tipo='software', palabras_clave='mysql,postgres,db', cliente=cliente_fixture),
        Activo.objects.create(nombre='Firewall', tipo='red', palabras_clave='cisco,firewall,router', cliente=cliente_fixture),
    ]
    return activos

@pytest.fixture
def cves_fixture(db):
    # Crear vulnerabilidades de ejemplo
    cves = [
        Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0001',
            descripcion_en='A vulnerability in Apache HTTP Server allows remote attackers...',
            descripcion_es='Una vulnerabilidad en Apache HTTP Server permite...',
            severidad='critica',
            status='published',
            fecha_publicacion='2024-06-01',
            fecha_modificacion='2024-06-01',
        ),
        Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0002',
            descripcion_en='A flaw in MySQL database engine...',
            descripcion_es='Un fallo en el motor de base de datos MySQL...',
            severidad='alta',
            status='published',
            fecha_publicacion='2024-06-02',
            fecha_modificacion='2024-06-02',
        ),
        Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0003',
            descripcion_en='A vulnerability in Cisco firewall devices...',
            descripcion_es='Una vulnerabilidad en dispositivos firewall Cisco...',
            severidad='media',
            status='published',
            fecha_publicacion='2024-06-03',
            fecha_modificacion='2024-06-03',
        ),
    ]
    return cves

class TestKeywordCorrelator:
    def test_correlacion_basica(self, activos_fixture, cves_fixture):
        correlator = KeywordCorrelator(severidad_minima='critica')
        correlator.correlate()
        relacion = ActivoVulnerabilidad.objects.filter(activo=activos_fixture[0], vulnerabilidad=cves_fixture[0]).first()
        alerta = Alerta.objects.filter(activo=activos_fixture[0], vulnerabilidad=cves_fixture[0]).first()
        assert relacion is not None, 'Debe crearse la relación ActivoVulnerabilidad'
        assert alerta is not None, 'Debe crearse la alerta si la severidad es suficiente'

    def test_no_correlacion(self, activos_fixture, cves_fixture):
        correlator = KeywordCorrelator(severidad_minima='critica')
        correlator.correlate()
        relacion = ActivoVulnerabilidad.objects.filter(activo=activos_fixture[1], vulnerabilidad=cves_fixture[0]).first()
        assert relacion is None, 'No debe crearse relación si no hay coincidencia'

    def test_umbral_severidad(self, activos_fixture, cves_fixture):
        correlator = KeywordCorrelator(severidad_minima='alta')
        correlator.correlate()
        alerta = Alerta.objects.filter(activo=activos_fixture[1], vulnerabilidad=cves_fixture[1]).first()
        assert alerta is not None, 'Debe crearse alerta si la severidad es igual al umbral'

    def test_no_alerta_por_severidad_baja(self, activos_fixture, cves_fixture):
        correlator = KeywordCorrelator(severidad_minima='alta')
        correlator.correlate()
        alerta = Alerta.objects.filter(activo=activos_fixture[2], vulnerabilidad=cves_fixture[2]).first()
        assert alerta is None, 'No debe crearse alerta si la severidad es inferior al umbral'
        relacion = ActivoVulnerabilidad.objects.filter(activo=activos_fixture[2], vulnerabilidad=cves_fixture[2]).first()
        assert relacion is not None, 'Debe crearse la relación aunque no haya alerta'

    def test_no_duplicidad_relacion(self, activos_fixture, cves_fixture):
        # Crear relación previa
        ActivoVulnerabilidad.objects.create(
            activo=activos_fixture[0], vulnerabilidad=cves_fixture[0],
            fecha_deteccion='2024-06-10', estado='PENDIENTE', notas='')
        correlator = KeywordCorrelator(severidad_minima='critica')
        correlator.correlate()
        relaciones = ActivoVulnerabilidad.objects.filter(activo=activos_fixture[0], vulnerabilidad=cves_fixture[0])
        assert relaciones.count() == 1, 'No debe haber duplicidad de relaciones'

    def test_no_duplicidad_alerta(self, activos_fixture, cves_fixture):
        # Crear alerta previa
        Alerta.objects.create(
            activo=activos_fixture[0], vulnerabilidad=cves_fixture[0],
            estado='nueva', notas='')
        correlator = KeywordCorrelator(severidad_minima='critica')
        correlator.correlate()
        alertas = Alerta.objects.filter(activo=activos_fixture[0], vulnerabilidad=cves_fixture[0])
        assert alertas.count() == 1, 'No debe haber duplicidad de alertas'

    def test_palabras_clave_insensibles_mayusculas_espacios(self, activos_fixture, cves_fixture):
        activos_fixture[0].palabras_clave = ' Apache , NGINX , Web '
        activos_fixture[0].save()
        correlator = KeywordCorrelator(severidad_minima='critica')
        correlator.correlate()
        relacion = ActivoVulnerabilidad.objects.filter(activo=activos_fixture[0], vulnerabilidad=cves_fixture[0]).first()
        assert relacion is not None, 'La correlación debe ser insensible a mayúsculas y espacios'

    def test_multiples_palabras_clave(self, activos_fixture, cves_fixture):
        activos_fixture[1].palabras_clave = 'mysql,postgres,db'
        activos_fixture[1].save()
        cves_fixture[1].descripcion_en = 'A flaw in the Postgres database engine...'
        cves_fixture[1].save()
        correlator = KeywordCorrelator(severidad_minima='alta')
        correlator.correlate()
        relacion = ActivoVulnerabilidad.objects.filter(activo=activos_fixture[1], vulnerabilidad=cves_fixture[1]).first()
        assert relacion is not None, 'Debe haber correlación si al menos una palabra clave coincide'

    def test_correlacion_filtrada_por_cves(self, activos_fixture, cves_fixture):
        # Solo pasamos la segunda CVE (MySQL)
        correlator = KeywordCorrelator(severidad_minima='alta', cves=[cves_fixture[1]])
        correlator.correlate()
        # Solo debe crearse la relación para la CVE filtrada
        relacion = ActivoVulnerabilidad.objects.filter(activo=activos_fixture[1], vulnerabilidad=cves_fixture[1]).first()
        assert relacion is not None, 'Debe crearse la relación solo para la CVE filtrada'
        # No debe crearse relación para las otras CVEs
        relacion_otro = ActivoVulnerabilidad.objects.filter(activo=activos_fixture[0], vulnerabilidad=cves_fixture[0]).first()
        assert relacion_otro is None, 'No debe crearse relación para CVEs no incluidas en la lista'