from django.test import TestCase
from django.utils import timezone
from vuln_manager.models.cliente.cliente import Cliente
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from vuln_manager.models.activo_vulnerabilidad.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository

class ActivoVulnerabilidadRepositoryTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombre='Cliente Test')
        self.activo = Activo.objects.create(
            cliente=self.cliente,
            nombre='Activo Test',
            tipo='hardware',
            palabras_clave='test'
        )
        self.vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0001',
            descripcion_en='Test vulnerability',
            descripcion_es='Vulnerabilidad de prueba',
            severidad='high',
            status='published',
            fecha_publicacion=timezone.now().date(),
            fecha_modificacion=timezone.now().date()
        )
        self.repository = ActivoVulnerabilidadRepository()

    def test_get_all(self):
        # Crear algunas relaciones con diferentes activos y vulnerabilidades
        activo2 = Activo.objects.create(
            cliente=self.cliente,
            nombre='Activo Test 2',
            tipo='software',
            palabras_clave='test2'
        )
        vulnerabilidad2 = Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0002',
            descripcion_en='Test vulnerability 2',
            descripcion_es='Vulnerabilidad de prueba 2',
            severidad='high',
            status='published',
            fecha_publicacion=timezone.now().date(),
            fecha_modificacion=timezone.now().date()
        )
        
        # Crear relaciones con diferentes combinaciones
        ActivoVulnerabilidad.objects.create(
            activo=self.activo,
            vulnerabilidad=self.vulnerabilidad,
            fecha_deteccion=timezone.now().date(),
            estado='PENDIENTE',
            notas='Notas de prueba 1'
        )
        
        ActivoVulnerabilidad.objects.create(
            activo=activo2,
            vulnerabilidad=vulnerabilidad2,
            fecha_deteccion=timezone.now().date(),
            estado='EN_PROGRESO',
            notas='Notas de prueba 2'
        )
        
        # Obtener todas las relaciones
        relaciones = self.repository.get_all()
        
        # Verificar que se obtuvieron todas las relaciones
        self.assertEqual(len(relaciones), 2)
        self.assertEqual(relaciones[0].estado, 'PENDIENTE')
        self.assertEqual(relaciones[1].estado, 'EN_PROGRESO')

    def test_get_by_id(self):
        # Crear una relación
        relacion = ActivoVulnerabilidad.objects.create(
            activo=self.activo,
            vulnerabilidad=self.vulnerabilidad,
            fecha_deteccion=timezone.now().date(),
            estado='PENDIENTE',
            notas='Notas de prueba'
        )
        
        # Obtener la relación por ID
        relacion_obtenida = self.repository.get_by_id(relacion.id)
        
        # Verificar que se obtuvo la relación correcta
        self.assertEqual(relacion_obtenida.id, relacion.id)
        self.assertEqual(relacion_obtenida.estado, 'PENDIENTE')
        self.assertEqual(relacion_obtenida.notas, 'Notas de prueba')

    def test_create(self):
        # Crear una nueva relación
        relacion = self.repository.create(
            activo=self.activo,
            vulnerabilidad=self.vulnerabilidad,
            fecha_deteccion=timezone.now().date(),
            estado='PENDIENTE',
            notas='Notas de prueba'
        )
        
        # Verificar que se creó correctamente
        self.assertIsNotNone(relacion.id)
        self.assertEqual(relacion.activo, self.activo)
        self.assertEqual(relacion.vulnerabilidad, self.vulnerabilidad)
        self.assertEqual(relacion.estado, 'PENDIENTE')
        self.assertEqual(relacion.notas, 'Notas de prueba')
        self.assertIsNotNone(relacion.created_at)
        self.assertIsNotNone(relacion.updated_at)

    def test_update(self):
        # Crear una relación
        relacion = ActivoVulnerabilidad.objects.create(
            activo=self.activo,
            vulnerabilidad=self.vulnerabilidad,
            fecha_deteccion=timezone.now().date(),
            estado='PENDIENTE',
            notas='Notas originales'
        )
        
        # Actualizar la relación
        relacion_actualizada = self.repository.update(
            relacion.id,
            estado='EN_PROGRESO',
            notas='Notas actualizadas'
        )
        
        # Verificar que se actualizó correctamente
        self.assertEqual(relacion_actualizada.estado, 'EN_PROGRESO')
        self.assertEqual(relacion_actualizada.notas, 'Notas actualizadas')
        self.assertIsNotNone(relacion_actualizada.updated_at)

    def test_delete(self):
        # Crear una relación
        relacion = ActivoVulnerabilidad.objects.create(
            activo=self.activo,
            vulnerabilidad=self.vulnerabilidad,
            fecha_deteccion=timezone.now().date(),
            estado='PENDIENTE',
            notas='Notas de prueba'
        )
        
        # Eliminar la relación
        self.repository.delete(relacion.id)
        
        # Verificar que se eliminó correctamente
        with self.assertRaises(ActivoVulnerabilidad.DoesNotExist):
            ActivoVulnerabilidad.objects.get(id=relacion.id) 