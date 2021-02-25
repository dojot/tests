from tests.base_test import BaseTest
from dojot.api import DojotAPI as Api
import json
import random
import time


class DeviceTest(BaseTest):

    def createTemplates(self, jwt: str, templates: list):
        template_ids = []
        for template in templates:
            rc, template_id = Api.create_template(jwt, json.dumps(template))

            template_ids.append(template_id["template"]["id"]) if rc == 200 else template_ids.append(None)
        return template_ids


    def createDevices(self, jwt: str, devices: list):
        result = []

        for templates, label in devices:
            self.logger.info('adding device ' + label + ' using templates ' + str(templates))
            rc, res = Api.create_device(jwt, templates, label)
            #self.assertTrue(rc == 200, "Error on create device")
            device_id = None
            if rc == 200:
                device_id = res["devices"][0]["id"]
            result.append((rc, res, device_id))
        return result


    def createDevicesWithParameters(self, jwt: str, template_id: int, label: str, attrs: str):
        rc, res = Api.create_devices_with_parameters(jwt, template_id, label, attrs)

        # return rc, res if rc != 200 else res
        return rc, res

    def updateDevice(self, jwt: str, device_id: str, template: str or dict):
        rc, res = Api.update_device(jwt, device_id, json.dumps(template))
        # self.assertTrue(isinstance(device_id, int), "Error on update device")
        return rc, res

    def getDevices(self, jwt: str):
        rc, res = Api.get_all_devices(jwt)
        # self.assertTrue(isinstance(device_id, int), "Error on get devices")
        return rc, res

    def getDevicesWithParameters(self, jwt: str, attrs: str):
        rc, res = Api.get_devices_with_parameters(jwt, attrs)
        # self.assertTrue(isinstance(device_id, int), "Error on get devices")
        return rc, res

    def getDevice(self, jwt: str, device_id: str):
        rc, res = Api.get_single_device(jwt, device_id)
        # self.assertTrue(isinstance(device_id, int), "Error on get device")
        return rc, res

    def deleteDevices(self, jwt: str):
        rc, res = Api.delete_devices(jwt)
        # self.assertTrue(isinstance(device_id, int), "Error on delete template")
        return rc, res

    def deleteDevice(self, jwt: str, device_id: str):
        rc, res = Api.delete_device(jwt, device_id)
        # self.assertTrue(isinstance(device_id, int), "Error on delete template")
        return rc, res

    def configureDevice(self, jwt: str, device_id: str, template: str or dict):
        rc, res = Api.configure_device(jwt, device_id, json.dumps(template))
        # self.assertTrue(isinstance(device_id, int), "Error on configure device")
        return rc, res

    def runTest(self):
        self.logger.info('Executing device test')
        self.logger.info('getting jwt...')
        jwt = Api.get_jwt()

        self.logger.info('listing all devices - no data...')
        rc, res = self.getDevices(jwt)
        self.logger.info(res)
        self.assertTrue(int(rc) == 200, "codigo inesperado")


        self.logger.info('creating template com todos os tipos de atributos...')

        templates = []
        self.logger.info('creating templates...')
        templates.append({
            "label": "Template",
            "attrs": [
                {
                    "label": "float",
                    "type": "dynamic",
                    "value_type": "float"
                },
                {
                    "label": "int",
                    "type": "dynamic",
                    "value_type": "integer"
                },
                {
                    "label": "text",
                    "type": "dynamic",
                    "value_type": "string"
                },
                {
                    "label": "gps",
                    "type": "dynamic",
                    "value_type": "geo:point",
                    "metadata": [
                        {
                            "label": "descricao",
                            "type": "static",
                            "value_type": "string",
                            "static_value": "localizacao do device"
                        }
                    ]
                },
                {
                    "label": "bool",
                    "type": "dynamic",
                    "value_type": "bool"
                },
                {
                    "label": "mensagem",
                    "type": "actuator",
                    "value_type": "string"
                },
                {
                    "label": "serial",
                    "type": "static",
                    "value_type": "string",
                    "static_value": "indefinido"
                },
                {
                    "label": "objeto",
                    "type": "dynamic",
                    "value_type": "object"
                }
            ]
        })
        templates.append({
            "label": "SensorModel",
            "attrs": [
                {
                    "label": "temperature",
                    "type": "dynamic",
                    "value_type": "float"
                },
                {
                    "label": "model-id",
                    "type": "static",
                    "value_type": "string",
                    "static_value": "model-001"
                }
                ]
        })
        templates.append({
            "label": "Temperature",
            "attrs": [
                {
                    "label": "temperature",
                    "type": "dynamic",
                    "value_type": "float"
                }
                ]
        })

        template_ids = self.createTemplates(jwt, templates)
        self.logger.info("templates ids: " + str(template_ids))

        devices = []
        devices.append(([template_ids[0]], "dispositivo"))
        devices.append(([template_ids[0]], "dispositivo2"))
        devices.append(([template_ids[1]], "sensor"))
        devices.append(([template_ids[1]], "sensor2"))
        devices_ids = self.createDevices(jwt, devices)
        self.logger.info("devices ids: " + str(devices_ids))

        self.logger.info('listing device - by ID...')
        rc, res = self.getDevice(jwt, Api.get_deviceid_by_label(jwt, 'sensor2'))
        self.logger.info('Device info: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        """
        Update device
        """

        self.logger.info('updating device sensor2: change of label and template......')
        template = {
            "label": "updated_device",
            "templates": [
                1
                ]
        }

        device_id = Api.get_deviceid_by_label(jwt, 'sensor2')

        rc, res = self.updateDevice(jwt, device_id, template)
        self.logger.info('Device updated: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing updated device...')
        rc, res = self.getDevice(jwt, device_id)
        self.logger.info('Device info: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('updating device dispositivo2: change of static and metadata values......')
        template = {
            "attrs": [
                {
                    "id": 4,
                    "label": "gps",
                    "metadata": [
                        {
                            "id": 9,
                            "label": "descricao",
                            "static_value": "posicao inicial",
                            "type": "static",
                            "value_type": "string"
                        }
                    ],
                    "template_id": "1",
                    "type": "dynamic",
                    "value_type": "geo:point"
                },
                {
                    "id": 7,
                    "label": "serial",
                    "static_value": "SN5242",
                    "template_id": "1",
                    "type": "static",
                    "value_type": "string"
                }
            ],
            "id": Api.get_deviceid_by_label(jwt, "dispositivo2"),
            "label": "dispositivo2",
            "templates": [1]
        }

        device_id = Api.get_deviceid_by_label(jwt, 'dispositivo2')

        rc, res = self.updateDevice(jwt, device_id, template)
        self.logger.info('Device updated: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing updated device...')
        rc, res = self.getDevice(jwt, device_id)
        self.logger.info('Device info: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        """
        Create multiple devices
        """

        self.logger.info('creating multiple devices...')
        rc, device_list = self.createDevicesWithParameters(jwt, template_ids[1], 'test_device', "count=5")
        self.logger.info('Devices created: ' + str(device_list))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('creating devices with verbose=False ...')
        rc, device_list = self.createDevicesWithParameters(jwt, template_ids[1], 'test_verbose_false', "verbose=False")
        self.logger.info('Device created: ' + str(device_list))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('creating devices with verbose=True ...')
        rc, device_list = self.createDevicesWithParameters(jwt, template_ids[1], 'test_verbose_true', "verbose=True")
        self.logger.info('Device created: ' + str(device_list))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        """
        Configure device - PUT /device/{id}/actuate
        """

        self.logger.info('configuring device: configuration sent to device......')
        template = {
            "attrs": {
                "mensagem": "atuando no device"
            }
        }

        device_id = Api.get_deviceid_by_label(jwt, 'dispositivo2')
        self.logger.info('device_id: ' + device_id)

        rc, res = self.configureDevice(jwt, device_id, template)
        self.logger.debug('Result: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")


        """
        Lista devices
        """

        self.logger.info('listing all devices...')
        rc, res = self.getDevices(jwt)
        self.logger.info('Device List: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: page_size=4...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_size=4")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: page_num=2...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_num=2")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: page_size=3&page_num=1...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_size=3&page_num=1")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: page_size=3&page_num=2...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_size=3&page_num=2")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: page_size=3&page_num=3...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_size=3&page_num=3")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: page_size=3&page_num=4...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_size=3&page_num=4")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: idsOnly=true...')
        rc, res = self.getDevicesWithParameters(jwt, "?idsOnly=true")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: idsOnly=false...')
        res = self.getDevicesWithParameters(jwt, "?idsOnly=false")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: attr...')  # só é válido para atributos estáticos
        rc, res = self.getDevicesWithParameters(jwt, "?attr=serial=indefinido")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: label...')
        rc, res = self.getDevicesWithParameters(jwt, "?label=test_device")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: sortBy...')
        rc, res = self.getDevicesWithParameters(jwt, "?sortBy=label")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: attr_type=integer...')
        rc, res = self.getDevicesWithParameters(jwt, "?attr_type=integer")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: attr_type=float...')
        rc, res = self.getDevicesWithParameters(jwt, "?attr_type=float")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: attr_type=string...')
        rc, res = self.getDevicesWithParameters(jwt, "?attr_type=string")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: attr_type=bool...')
        rc, res = self.getDevicesWithParameters(jwt, "?attr_type=bool")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: attr_type=geo:point...')
        rc, res = self.getDevicesWithParameters(jwt, "?attr_type=geo:point")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameter: attr_type=object...')
        rc, res = self.getDevicesWithParameters(jwt, "?attr_type=object")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with all parameters...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_size=2&page_num=1&idsOnly=true&attr_type=string&attr=serial=indefinido&label=dispositivo&sortBy=label")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameters (no match): return empty...')
        rc, res = self.getDevicesWithParameters(jwt,
                                            "?page_size=2&page_num=1&idsOnly=false&attr_type=string&attr=serial=undefined&label=device&sortBy=label")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices with parameters (nonexistent parameter ): return full...')
        rc, res = self.getDevicesWithParameters(jwt, "?parametro=outro")
        self.logger.info('Devices: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices associated with given template...')
        rc, res = self.getDevicesWithParameters(jwt, "/template/1")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices associated with given template - page_num...')
        rc, res = self.getDevicesWithParameters(jwt, "/template/1?page_num=1")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices associated with given template - page_size...')
        rc, res = self.getDevicesWithParameters(jwt, "/template/1?page_size=2")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing devices associated with given template - page_num e page_size...')
        rc, res = self.getDevicesWithParameters(jwt, "/template/1?page_size=2&page_num=2")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        """
        Lista device especifico
        """

        self.logger.info('listing specific device - device_id...')
        rc, res = self.getDevice(jwt, Api.get_deviceid_by_label(jwt, 'sensor'))
        self.logger.info('Device info: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing specific device - label...')
        rc, res = self.getDevicesWithParameters(jwt, '?label=dispositivo')
        self.logger.info('Device info: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        """
        Remove device especifico
        """

        device_id = Api.get_deviceid_by_label(jwt, 'test_device_4')

        self.logger.info('removing specific device...')
        rc, res = self.deleteDevice(jwt, str(device_id))
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")


        """
        Remove all devices
        """

        """
        self.logger.info('removing all devices...')
        res = self.deleteDevices(jwt)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")
        """

        """
        Fluxos Alternativos
        """

        """
        POST
        """

        self.logger.info('creating device - No such template...')

        devices = []
        devices.append(("1000", "teste"))
        result = self.createDevices(jwt, devices)
        self.logger.info("Result: " + str(result))
        self.assertTrue(int(result[0][0]) == 404, "codigo inesperado")

        self.logger.info('creating devices with count & verbose ...- Verbose can only be used for single device creation')
        rc, result = self.createDevicesWithParameters(jwt, template_ids[1], 'test', "count=3&verbose=true")
        self.logger.info('Result: ' + str(result))
        self.assertTrue(int(rc) == 400, "codigo inesperado")

        self.logger.info('creating devices - count must be integer ...')
        rc, result = self.createDevicesWithParameters(jwt, template_ids[1], 'test', "count=true")
        self.logger.info('Result: ' + str(result))
        self.assertTrue(int(rc) == 400, "codigo inesperado")

        #TODO: 'creating devices - Payload must be valid JSON...' (tem como provocar o erro?) ex: {"templates", "label": "dev"}

        #TODO: 'creating devices - Missing data for required field ...' ex: {"template": [1]}


        #'a device can not have repeated attributes' (device tem 2 atributos iguais de templates diferentes)
        devices = []
        devices.append(([template_ids[1], template_ids[2]], "repeated attributes"))
        result = self.createDevices(jwt, devices)
        self.logger.info("Result: " + str(result))
        self.assertTrue(int(result[0][0]) == 400, "codigo inesperado")

        #TODO: 'Failed to generate unique device_id' (é erro interno)

        """
        GET
        """

        self.logger.info('listing device - No such device...')
        rc, res = self.getDevice(jwt, "123")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 404, "codigo inesperado")

        self.logger.info('listing device - internal error...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_num=")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 500, "codigo inesperado")

        self.logger.info('listing devices with parameter: Page numbers must be greater than 1...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_num=0")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 400, "codigo inesperado")

        self.logger.info('listing devices with parameter: At least one entry per page is mandatory...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_size=0")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 400, "codigo inesperado")

        self.logger.info('listing devices with parameter: page_size and page_num must be integers...')
        rc, res = self.getDevicesWithParameters(jwt, "?page_num=xyz&page_size=kwv")
        self.logger.info('Result: ' + str(res))
        #self.assertTrue(int(rc) == 400, "codigo inesperado")  ## erro esperado
        self.assertTrue(int(rc) == 500, "codigo inesperado")

        """
        GET - list of devices associated with given template
        GET/device/template/{template_id}{?page_size,page_num}
        """
        self.logger.info('listing devices associated with given template - At least one entry per page is mandatory...')
        rc, res = self.getDevicesWithParameters(jwt, "/template/1?page_size=0")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 400, "codigo inesperado")

        self.logger.info('listing devices associated with given template - Page numbers must be greater than 1...')
        rc, res = self.getDevicesWithParameters(jwt, "/template/1?page_num=0")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 400, "codigo inesperado")

        self.logger.info('listing devices associated with given template - page_size and page_num must be integers...')
        rc, res = self.getDevicesWithParameters(jwt, "/template/1?page_num=kwv&page_size=xyz")
        self.logger.info('Result: ' + str(res))
        #self.assertTrue(int(rc) == 400, "codigo inesperado")  ## erro esperado
        self.assertTrue(int(rc) == 500, "codigo inesperado")


        """
        PUT  /device/{id}
        """



        # TODO: 'updating device - Payload must be valid JSON, and Content-Type set accordingly'


        self.logger.info('updating device: Missing data for required field......')
        template = {}

        device_id = Api.get_deviceid_by_label(jwt, 'test_device_1')

        rc, res = self.updateDevice(jwt, device_id, template)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 400, "codigo inesperado")


        self.logger.info('updating device: a device can not have repeated attributes......')
        template = {
            "label": "test_device_1",
            "templates": [template_ids[1], template_ids[2]]
        }

        device_id = Api.get_deviceid_by_label(jwt, 'test_device_1')

        rc, res = self.updateDevice(jwt, device_id, template)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 400, "codigo inesperado")

        self.logger.info('updating device: No such device: aaaa......')
        template = {
            "label": "teste_device_1",
            "templates": [template_ids[1]]
        }

        rc, res = self.updateDevice(jwt, 'aaaa', template)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 404, "codigo inesperado")

        self.logger.info('updating device: No such template: 4685......')
        template = {
            "label": "teste_device_1",
            "templates": [4685]
        }

        device_id = Api.get_deviceid_by_label(jwt, 'test_device_1')

        rc, res = self.updateDevice(jwt, device_id, template)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 404, "codigo inesperado")

        self.logger.info('updating device: Unknown template 4865 in attr list......')

        template = {
            "label": "teste_device_0",
            "templates": [template_ids[1], template_ids[2], 4732]
        }

        device_id = Api.get_deviceid_by_label(jwt, 'test_device_0')

        rc, res = self.updateDevice(jwt, device_id, template)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 404, "codigo inesperado")

        self.logger.info('updating device: missing label attribute......')


        template = {
            "attrs": [
                {
                    "id": 7,
                    "static_value": "SN1000",
                    "template_id": "1",
                    "type": "static",
                    "value_type": "string"
                }
            ],
            "id": Api.get_deviceid_by_label(jwt, "dispositivo2"),
            "label": "dispositivo2",
            "templates": [1]
        }

        device_id = Api.get_deviceid_by_label(jwt, 'dispositivo2')

        rc, res = self.updateDevice(jwt, device_id, template)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 400, "codigo inesperado")

        # TODO: 'updating device - Unknown attribute 2 in override list'

        # TODO: 'updating device - Unknown metadata attribute 2 in override list'


        """
        Configure device - PUT /device/{id}/actuate
        """

        self.logger.info('configuring device: No such device: aaaa......')
        template = {
            "attrs": {
                "mensagem": "NOK"
            }
        }

        rc, res = self.configureDevice(jwt, 'aaaa', template)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 404, "codigo inesperado")

        self.logger.info('configuring device: some of the attributes are not configurable......')
        template = {
            "attrs": {
                "float": 1.5
            }
        }

        device_id = Api.get_deviceid_by_label(jwt, 'dispositivo')

        rc, res = self.configureDevice(jwt, device_id, template)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 403, "codigo inesperado")

        """
        DELETE
        """

        self.logger.info('removing specific device - No such device...')
        rc, res = self.deleteDevice(jwt, '123')
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 404, "codigo inesperado")


        """
        Remove all devices
        """
        """

        self.logger.info('removing all devices...')
        rc, res = self.deleteDevices(jwt)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")
        """

