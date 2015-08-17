from cityfarm_api.test import APITestCase, run_with_any_layout
from cityfarm_api.serializers import model_serializers
from .models import ResourceType, ResourceProperty, Resource

class ResourceTypeTestCase(APITestCase):
    @run_with_any_layout
    def test_visible_fields(self):
        ResourceTypeSerializer = model_serializers.get_for_model(ResourceType)
        fields = ResourceTypeSerializer().get_fields()
        fields.pop('url')
        fields.pop('code')
        fields.pop('name')
        fields.pop('read_only')
        fields.pop('resource_count')
        fields.pop('properties')
        fields.pop('resources')
        fields.pop('sensor_types')
        fields.pop('actuator_types')
        self.assertFalse(fields)

    @run_with_any_layout
    def test_edit_stock_type(self):
        data = {'code': 'A', 'name': 'test'}
        air_id = ResourceType.objects.get_by_natural_key('A').pk
        res = self.client.put(
            self.url_for_object('resourceType', air_id), data=data
        )
        self.assertEqual(res.status_code, 403)

    @run_with_any_layout
    def test_edit_custom_type(self):
        data = {'code': 'T', 'name': 'test'}
        res = self.client.post(self.url_for_object('resourceType'), data=data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['name'], 'test')
        data['name'] = 'test2'
        res = self.client.put(res.data['url'], data=data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['name'], 'test2')

    @run_with_any_layout
    def test_invalid_code(self):
        data = {'code': '', 'name': 'test'}
        res = self.client.post(self.url_for_object('resourceType'), data=data)
        self.assertEqual(res.status_code, 400)
        data['code'] = 'TS'
        res = self.client.post(self.url_for_object('resourceType'), data=data)
        self.assertEqual(res.status_code, 400)


class ResourcePropertyTestCase(APITestCase):
    @run_with_any_layout
    def test_visible_fields(self):
        ResourcePropertySerializer = model_serializers.get_for_model(
            ResourceProperty
        )
        fields = ResourcePropertySerializer().get_fields()
        fields.pop('url')
        fields.pop('code')
        fields.pop('name')
        fields.pop('resource_type')
        fields.pop('read_only')
        fields.pop('sensing_point_count')
        fields.pop('sensing_points')
        fields.pop('sensor_types')
        fields.pop('actuator_types')
        self.assertFalse(fields)

    @run_with_any_layout
    def test_edit_stock_property(self):
        air_id = ResourceType.objects.get_by_natural_key('A').pk
        air_temp_id = ResourceProperty.objects.get_by_natural_key(
            'A', 'TM'
        ).pk
        data = {
            'code': 'ATS',
            'name': 'Air Test',
            'resource_type': self.url_for_object('resourceType', air_id)
        }
        res = self.client.put(
            self.url_for_object('resourceProperty', air_temp_id), data=data
        )
        self.assertEqual(res.status_code, 403)

    @run_with_any_layout
    def test_edit_custom_property(self):
        air_id = ResourceType.objects.get_by_natural_key('A').pk
        data = {
            'code': 'TS',
            'name': 'Air Test',
            'resource_type': self.url_for_object('resourceType', air_id)
        }
        res = self.client.post(
            self.url_for_object('resourceProperty'), data=data
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['name'], 'Air Test')
        data['name'] = 'Air Test2'
        res = self.client.put(res.data['url'], data=data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['name'], 'Air Test2')

    @run_with_any_layout
    def test_invalid_code(self):
        air_id = ResourceType.objects.get_by_natural_key('A').pk
        data = {
            'code': 'A', 'name': 'test', 'resource_type':
            self.url_for_object('resourceType', air_id)
        }
        res = self.client.post(
            self.url_for_object('resourceProperty'), data=data
        )
        self.assertEqual(res.status_code, 400)
        data['code'] = 'ABC'
        res = self.client.post(
            self.url_for_object('resourceProperty'), data=data
        )
        self.assertEqual(res.status_code, 400)


class ResourceTestCase(APITestCase):
    @run_with_any_layout
    def test_visible_fields(self):
        ResourceSerializer = model_serializers.get_for_model(Resource)
        fields = ResourceSerializer().get_fields()
        fields.pop('url')
        fields.pop('index')
        fields.pop('name')
        fields.pop('resource_type')
        fields.pop('location')
        fields.pop('sensors')
        fields.pop('actuators')
        self.assertFalse(fields)

    @run_with_any_layout
    def test_resource_creation(self):
        air_id = ResourceType.objects.get_by_natural_key('A').pk
        # Create the resource
        data = {
            'resource_type': self.url_for_object('resourceType', air_id),
            'location': self.url_for_object('enclosure', 1),
        }
        res = self.client.post(self.url_for_object('resource'), data=data)
        self.assertEqual(res.status_code, 201)
        # Validate the index and name
        resource_type = self.client.get(data['resource_type']).data
        num_resources = resource_type['resource_count']
        self.assertEqual(res.data['index'], num_resources)
        expected_name = "{} Resource {}".format(
            resource_type['name'], num_resources
        )
        self.assertEqual(res.data['name'], expected_name)
        # Change the name
        data['name'] = 'test'
        res = self.client.put(res.data['url'], data=data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['name'], 'test')
        # Try changing the type
        water_id = ResourceType.objects.get_by_natural_key('W').pk
        data['resource_type'] = self.url_for_object('resourceType', water_id)
        res = self.client.put(res.data['url'], data=data)
        self.assertEqual(res.status_code, 400)
