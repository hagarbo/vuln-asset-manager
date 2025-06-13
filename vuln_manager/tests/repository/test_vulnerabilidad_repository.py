from django.test import TestCase
from vuln_manager.repository.vulnerabilidad import VulnerabilidadRepository
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad

class TestVulnerabilidadRepository(TestCase):
    """
    Tests específicos para el repositorio de Vulnerabilidades.
    """
    def setUp(self):
        """Configuración inicial para cada test."""
        self.repository = VulnerabilidadRepository()
        self.vulnerabilidad_data = {
            'cve_id': 'CVE-2024-0001',
            'descripcion_en': 'Test vulnerability EN',
            'descripcion_es': 'Test vulnerabilidad ES',
            'severidad': 'alta',
            'status': 'published',
            'fecha_publicacion': '2024-01-01',
            'fecha_modificacion': '2024-01-01'
        }
        self.vulnerabilidad = self.repository.create(**self.vulnerabilidad_data)

    def test_create_vulnerabilidad(self):
        """Test para crear una vulnerabilidad con todos sus campos."""
        # Crear una nueva vulnerabilidad con cve_id diferente
        new_data = self.vulnerabilidad_data.copy()
        new_data['cve_id'] = 'CVE-2024-0004'
        new_vuln = self.repository.create(**new_data)
        
        # Verificar que se creó correctamente
        self.assertIsNotNone(new_vuln.id)
        self.assertEqual(new_vuln.cve_id, new_data['cve_id'])
        self.assertEqual(new_vuln.descripcion_es, new_data['descripcion_es'])
        self.assertEqual(new_vuln.descripcion_en, new_data['descripcion_en'])

    def test_get_vulnerabilidad_by_cve(self):
        """Test para obtener una vulnerabilidad por su CVE ID."""
        # Obtener la vulnerabilidad por ID
        vuln = self.repository.get_by_id(self.vulnerabilidad.id)
        
        # Verificar que es la vulnerabilidad correcta
        self.assertEqual(vuln.cve_id, self.vulnerabilidad_data['cve_id'])

    def test_update_vulnerabilidad(self):
        """Test para actualizar una vulnerabilidad."""
        # Datos de actualización
        update_data = {
            'descripcion_es': 'Descripción actualizada',
            'descripcion_en': 'Updated description',
            'severidad': 'critica'
        }
        
        # Actualizar la vulnerabilidad
        updated_vuln = self.repository.update(self.vulnerabilidad.id, **update_data)
        
        # Verificar que se actualizó correctamente
        self.assertEqual(updated_vuln.descripcion_es, update_data['descripcion_es'])
        self.assertEqual(updated_vuln.descripcion_en, update_data['descripcion_en'])
        self.assertEqual(updated_vuln.severidad, update_data['severidad'])

    def test_delete_vulnerabilidad(self):
        """Test para eliminar una vulnerabilidad."""
        # Eliminar la vulnerabilidad
        result = self.repository.delete(self.vulnerabilidad.id)
        
        # Verificar que se eliminó correctamente
        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id(self.vulnerabilidad.id)) 