from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from ..gro_api.test import APITestCase, run_with_any_layout
from ..resources.models import ResourceType, ResourceProperty
from .models import SensorType, Sensor, SensingPoint, DataPoint
from .serializers import SensorTypeSerializer, SensorSerializer

class SensorAuthMixin:
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            'sensors', 'sensors@test.com', 'sensors'
        )
        electricians_group = Group.objects.get(name='Electricians')
        cls.user.groups.add(electricians_group)
        layout_editors_group = Group.objects.get(name='LayoutEditors')
        cls.user.groups.add(layout_editors_group)

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.force_authenticate()

class SensorTypeTestCase(SensorAuthMixin, APITestCase):
    @run_with_any_layout
    def test_visible_fields(self):
        fields = SensorTypeSerializer().get_fields()
        fields.pop('url')
        fields.pop('name')
        fields.pop('resource_type')
        fields.pop('properties')
        fields.pop('read_only')
        fields.pop('sensor_count')
        fields.pop('sensors')
        self.assertFalse(fields)

    @run_with_any_layout
    def test_edit_stock_type(self):
        air_id = ResourceType.objects.get_by_natural_key('A').pk
        air_temp_id = ResourceProperty.objects.get_by_natural_key('A', 'TM').pk
        data = {
            'name': 'test',
            'resource_type': self.url_for_object('resourceType', air_id),
            'properties': [
                self.url_for_object('resourceProperty', air_temp_id)
            ]
        }
        dht22_id = SensorType.objects.get_by_natural_key('DHT22').pk
        res = self.client.put(
            self.url_for_object('sensorType', dht22_id), data=data
        )
        self.assertEqual(res.status_code, 403)

    @run_with_any_layout
    def test_edit_custom_type(self):
        air_id = ResourceType.objects.get_by_natural_key('A').pk
        air_temp_id = ResourceProperty.objects.get_by_natural_key('A', 'TM').pk
        data = {
            'name': 'test',
            'resource_type': self.url_for_object('resourceType', air_id),
            'properties': [
                self.url_for_object('resourceProperty', air_temp_id)
            ]
        }
        res = self.client.post(self.url_for_object('sensorType'), data=data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['name'], 'test')
        data['name'] = 'test2'
        res = self.client.put(res.data['url'], data=data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['name'], 'test2')

    @run_with_any_layout
    def test_invalid_properties(self):
        water_id = ResourceType.objects.get_by_natural_key('W').pk
        air_temp_id = ResourceProperty.objects.get_by_natural_key('A', 'TM').pk
        data = {
            'name': 'test',
            'resource_type': self.url_for_object('resourceType', water_id),
            'properties': [
                self.url_for_object('resourceProperty', air_temp_id)
            ]
        }
        res = self.client.post(self.url_for_object('sensorType'), data=data)
        self.assertEqual(res.status_code, 400)


class SensorTestCase(SensorAuthMixin, APITestCase):
    @run_with_any_layout
    def test_visible_fields(self):
        fields = SensorSerializer().get_fields()
        fields.pop('url')
        fields.pop('index')
        fields.pop('name')
        fields.pop('sensor_type')
        fields.pop('resource')
        fields.pop('is_active')
        fields.pop('sensing_points')
        self.assertFalse(fields)

    @run_with_any_layout
    def test_sensor_creation(self):
        # Create a resource to install the sensor in
        air_id = ResourceType.objects.get_by_natural_key('A').pk
        resource_info = {
            'resource_type': self.url_for_object('resourceType', air_id),
            'location': self.url_for_object('enclosure', 1)
        }
        res = self.client.post(
            self.url_for_object('resource'), data=resource_info
        )
        self.assertEqual(res.status_code, 201)
        resource = res.data
        # Create the sensor
        dht22_id = SensorType.objects.get_by_natural_key('DHT22').pk
        sensor_info = {
            'sensor_type': self.url_for_object('sensorType', dht22_id),
            'resource': resource['url']
        }
        res = self.client.post(self.url_for_object('sensor'), data=sensor_info)
        self.assertEqual(res.status_code, 201)
        sensor = res.data
        # Validate the index and name
        res = self.client.get(sensor['sensor_type'])
        self.assertEqual(res.status_code, 200)
        sensor_type = res.data
        num_sensors = sensor_type['sensor_count']
        self.assertEqual(sensor['index'], num_sensors)
        expected_name = "{} Instance {}".format(
            sensor_type['name'], num_sensors
        )
        self.assertEqual(sensor['name'], expected_name)
        # Validate the sensing points
        properties = list(sensor_type['properties'])
        for sensing_point_url in sensor['sensing_points']:
            res = self.client.get(sensing_point_url)
            self.assertEqual(res.status_code, 200)
            sensing_point = res.data
            self.assertEqual(sensing_point['sensor'], sensor['url'])
            properties.remove(sensing_point['property'])
        self.assertFalse(properties)
        # Change the name
        sensor_info['name'] = 'test'
        res = self.client.put(sensor['url'], data=sensor_info)
        self.assertEqual(res.status_code, 200)
        sensor = res.data
        self.assertEqual(sensor['name'], 'test')
        # Try changing the type
        old_sensor_type_url = sensor_info['sensor_type']
        gc0011_id = SensorType.objects.get_by_natural_key('GC0011').pk
        sensor_info['sensor_type'] = self.url_for_object(
            'sensorType', gc0011_id
        )
        res = self.client.put(sensor['url'], data=sensor_info)
        self.assertEqual(res.status_code, 400)
        sensor_info['sensor_type'] = old_sensor_type_url
        # Create a new resource of a different type
        water_id = ResourceType.objects.get_by_natural_key('W').pk
        new_resource_info = {
            'resource_type': self.url_for_object('resourceType', water_id),
            'location': self.url_for_object('enclosure', 1)
        }
        res = self.client.post(
            self.url_for_object('resource'), data=new_resource_info
        )
        self.assertEqual(res.status_code, 201)
        new_resource = res.data
        # Try to move the sensor to the new resource
        sensor_info['resource'] = new_resource['url']
        res = self.client.put(sensor['url'], data=sensor_info)
        self.assertEqual(res.status_code, 400)


class SensingPointTestCase(APITestCase):
    # TODO: Test data routes
    pass
