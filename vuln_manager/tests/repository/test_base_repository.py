from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad

class TestBaseRepository(TestCase):
    """
    Tests para el BaseRepository.
    Usamos el modelo Vulnerabilidad como ejemplo para probar la funcionalidad base.
    """
    def setUp(self):
        """Configuración inicial para cada test."""
        self.repository = BaseRepository(Vulnerabilidad)
        self.vulnerabilidad_data = {
            'cve_id': 'CVE-2024-0001',
            'descripcion_es': 'Test vulnerabilidad',
            'severidad': 'alta',
            'status': 'published',
            'fecha_publicacion': '2024-01-01',
            'fecha_modificacion': '2024-01-01'
        }
        self.vulnerabilidad = self.repository.create(**self.vulnerabilidad_data)

    def test_get_all(self):
        """Test para obtener todos los objetos."""
        # Crear una segunda vulnerabilidad con cve_id diferente
        second_data = self.vulnerabilidad_data.copy()
        second_data['cve_id'] = 'CVE-2024-0002'
        self.repository.create(**second_data)
        
        # Verificar que get_all devuelve todos los objetos
        all_objects = self.repository.get_all()
        self.assertEqual(all_objects.count(), 2)

    def test_get_by_id(self):
        """Test para obtener un objeto por su ID."""
        # Obtener la vulnerabilidad por ID
        obj = self.repository.get_by_id(self.vulnerabilidad.id)
        
        # Verificar que es el objeto correcto
        self.assertEqual(obj.cve_id, self.vulnerabilidad_data['cve_id'])
        self.assertEqual(obj.descripcion_es, self.vulnerabilidad_data['descripcion_es'])

    def test_get_by_id_not_found(self):
        """Test para obtener un objeto que no existe."""
        # Intentar obtener un objeto con ID inexistente
        obj = self.repository.get_by_id(99999)
        
        # Verificar que devuelve None
        self.assertIsNone(obj)

    def test_create(self):
        """Test para crear un nuevo objeto."""
        # Crear una nueva vulnerabilidad con cve_id diferente
        new_data = {
            'cve_id': 'CVE-2024-0003',
            'descripcion_es': 'Nueva vulnerabilidad',
            'severidad': 'media',
            'status': 'draft',
            'fecha_publicacion': '2024-01-02',
            'fecha_modificacion': '2024-01-02'
        }
        obj = self.repository.create(**new_data)
        
        # Verificar que se creó correctamente
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.cve_id, new_data['cve_id'])
        self.assertEqual(obj.descripcion_es, new_data['descripcion_es'])

    def test_update(self):
        """Test para actualizar un objeto existente."""
        # Datos de actualización
        update_data = {
            'descripcion_es': 'Descripción actualizada',
            'severidad': 'critica'
        }
        
        # Actualizar el objeto
        updated_obj = self.repository.update(self.vulnerabilidad.id, **update_data)
        
        # Verificar que se actualizó correctamente
        self.assertEqual(updated_obj.descripcion_es, update_data['descripcion_es'])
        self.assertEqual(updated_obj.severidad, update_data['severidad'])

    def test_update_not_found(self):
        """Test para actualizar un objeto que no existe."""
        # Intentar actualizar un objeto inexistente
        result = self.repository.update(99999, descripcion_es='No debería actualizarse')
        
        # Verificar que devuelve None
        self.assertIsNone(result)

    def test_delete(self):
        """Test para eliminar un objeto."""
        # Eliminar el objeto
        result = self.repository.delete(self.vulnerabilidad.id)
        
        # Verificar que se eliminó correctamente
        self.assertTrue(result)
        # Verificar que no se puede obtener el objeto eliminado
        self.assertIsNone(self.repository.get_by_id(self.vulnerabilidad.id))

    def test_delete_not_found(self):
        """Test para eliminar un objeto que no existe."""
        # Intentar eliminar un objeto inexistente
        result = self.repository.delete(99999)
        
        # Verificar que devuelve False
        self.assertFalse(result) 