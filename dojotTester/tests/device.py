from tests.base_test import BaseTest
from dojot.api import DojotAPI as Api
import json
import random
import time


class DeviceTest(BaseTest):



    def createSingleDevice(self, jwt: str, template_id: int, label: str):
        device_ids = []

        #for templates, label in devices:
        #self.logger.info('adding device ' + label + ' using templates ' + str(templates))
        rc, res = Api.create_single_device(jwt, template_id, label)
        #self.assertTrue(device_id is not None, "Error on create device")
        #device_ids.append(device_id) if rc == 200 else device_ids.append(None)

        return rc, res if rc==200 else res


    def createDeviceFail(self, jwt: str, template_id: int, label: str):
        rc, res = Api.create_device(jwt, template_id, label)

        # return rc, res if rc != 200 else res
        return res

    def createMultipleDevices(self, jwt: str, template_id: int, label: str, attrs: str):
        rc, res = Api.create_multiple_devices(jwt, template_id, label, attrs)

        # return rc, res if rc != 200 else res
        return res

    def updateDevice(self, jwt: str, device_id: int, template: str):
        rc, res = Api.update_device(jwt, device_id, json.dumps(template))
        # self.assertTrue(isinstance(device_id, int), "Error on update device")
        return res if rc == 200 else res

    def getDevices(self, jwt: str):
        rc, res = Api.get_all_devices(jwt)
        # self.assertTrue(isinstance(device_id, int), "Error on get devices")
        return res

    def getDevicesWithParameters(self, jwt: str, attrs: str):
        res = Api.get_devices_with_parameters(jwt, attrs)
        # self.assertTrue(isinstance(device_id, int), "Error on get devices")
        return res

    def getDevice(self, jwt: str, device_id: str):
        res = Api.get_single_device(jwt, device_id)
        # self.assertTrue(isinstance(device_id, int), "Error on get device")
        return res

    def deleteDevices(self, jwt: str):
        res = Api.delete_devices(jwt)
        # self.assertTrue(isinstance(device_id, int), "Error on delete template")
        return res

    def deleteDevice(self, jwt: str, device_id: int):
        res = Api.delete_device(jwt, device_id)
        # self.assertTrue(isinstance(device_id, int), "Error on delete template")
        return res

    def runTest(self):
        self.logger.info('Executing device test')
        self.logger.debug('getting jwt...')
        jwt = Api.get_jwt()

        self.logger.info('listing all devices...')
        res = self.getDevices(jwt)
        self.logger.debug(res)


        self.logger.info('creating template com todos os tipos de atributos...')
        template = {
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
        }

        rc, template_id = Api.create_template(jwt, template)
        self.logger.info('Template created: ' + str(template_id) + ', Template')

        device_id = self.createSingleDevice(jwt, template_id, 'dispositivo')
        self.logger.info('Device created: ' + str(device_id))

        #TODO: 'listing device - by ID...'

        """
        self.logger.info('listing device - by ID...')
        list = self.getDevice(jwt, '82bbef')
        self.logger.info('Device info: ' + str(list))
        """

        self.logger.info('listing device - by label...')
        list = self.getDevice(jwt, 'label=dispositivo')
        self.logger.info('Device info: ' + str(list))

        """
          
        self.logger.debug('updating device ......')
        template = {
            "label": "dispositivo",
            "attrs": [
                {
                    "label": "serial",
                    "type": "static",
                    "value_type": "string",
                    "static_value": "0001"
                }
            ]
        }

        rc, res = self.updateDevice(jwt, device_id, template)
        self.logger.info('Device updated: ' + str(device_id))

        self.logger.info('listing updated template...')
        list = self.getDevice(jwt, device_id)
        self.logger.info('Device info: ' + str(list))
        """

        """
        Create multiple devices
        """

        self.logger.info('creating multiple devices...')
        device_list = self.createMultipleDevices(jwt, template_id, 'test_device', "count=5")
        self.logger.info('Devices created: ' + str(device_list))

        self.logger.info('creating devices with verbose=False ...')
        device_list = self.createMultipleDevices(jwt, template_id, 'test_verbose_false', "verbose=False")
        self.logger.debug('Device created: ' + str(device_list))

        self.logger.info('creating devices with verbose=True ...')
        device_list = self.createMultipleDevices(jwt, template_id, 'test_verbose_true', "verbose=True")
        self.logger.debug('Device created: ' + str(device_list))

        """
        #Lista devices
        """

        self.logger.info('listing all devices...')
        list = self.getDevices(jwt)
        self.logger.debug('Device List: ' + str(list))

        self.logger.info('listing devices with parameter: page_size...')
        res = self.getDevicesWithParameters(jwt, "page_size=3")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: page_num...')
        res = self.getDevicesWithParameters(jwt, "page_num=2")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: page_size=2&page_num=1...')
        res = self.getDevicesWithParameters(jwt, "page_size=2&page_num=1")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: page_size=2&page_num=2...')
        res = self.getDevicesWithParameters(jwt, "page_size=2&page_num=2")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: page_size=2&page_num=3...')
        res = self.getDevicesWithParameters(jwt, "page_size=2&page_num=3")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: page_size=2&page_num=4...')
        res = self.getDevicesWithParameters(jwt, "page_size=2&page_num=4")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: idsOnly=true...')
        res = self.getDevicesWithParameters(jwt, "idsOnly=true")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: idsOnly=false...')
        res = self.getDevicesWithParameters(jwt, "idsOnly=false")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr...')  # só é válido para atributos estáticos
        res = self.getDevicesWithParameters(jwt, "attr=serial=indefinido")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: label...')
        res = self.getDevicesWithParameters(jwt, "label=test_device")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: sortBy...')
        res = self.getDevicesWithParameters(jwt, "sortBy=label")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=integer...')
        res = self.getDevicesWithParameters(jwt, "attr_type=integer")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=float...')
        res = self.getDevicesWithParameters(jwt, "attr_type=float")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=string...')
        res = self.getDevicesWithParameters(jwt, "attr_type=string")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=bool...')
        res = self.getDevicesWithParameters(jwt, "attr_type=bool")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=geo:point...')
        res = self.getDevicesWithParameters(jwt, "attr_type=geo:point")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=object...')
        res = self.getDevicesWithParameters(jwt, "attr_type=object")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with all parameters...')
        res = self.getDevicesWithParameters(jwt, "page_size=2&page_num=1&idsOnly=true&attr_type=string&attr=serial=indefinido&label=dispositivo&sortBy=label")
        self.logger.info('Devices: ' + str(res))

        self.logger.info('listing devices with parameters (no match): return empty...')
        res = self.getDevicesWithParameters(jwt,
                                            "page_size=2&page_num=1&idsOnly=false&attr_type=string&attr=serial=undefined&label=device&sortBy=label")
        self.logger.info('Devices: ' + str(res))

        self.logger.info('listing devices with parameters (nonexistent parameter ): return full...')
        res = self.getDevicesWithParameters(jwt, "parametro=outro")
        self.logger.debug('Devices: ' + str(res))

        """
        Lista device especifico
        """

        self.logger.info('listing specific device - device_id...')
        res = self.getDevice(jwt, '5a201d')
        self.logger.debug('Device info: ' + str(res))

        self.logger.info('listing specific device - label...')
        res = self.getDevice(jwt, '?label=dispositivo')
        self.logger.debug('Device info: ' + str(res))

        """
        Remove device especifico
        """
        """

        self.logger.info('removing specific device - device_id...')
        res = self.deleteDevice(jwt, device_id)
        self.logger.info('Result: ' + str(res))

        self.logger.info('removing specific device - label...')
        res = self.deleteDevice(jwt, 'test_device_0')
        self.logger.info('Result: ' + str(res))
       """

        """
        Remove all devices
        """

        """
        self.logger.info('removing all devices...')
        res = self.deleteDevices(jwt)
        self.logger.debug('Result: ' + str(res))
        """

        """
        Fluxos Alternativos
        """
        self.logger.info('creating devices with count & verbose ...')
        result = self.createMultipleDevices(jwt, template_id, 'test', "count=3&verbose=true")
        self.logger.info('Result: ' + str(result))

        self.logger.info('creating devices - count must be integer ...')
        result = self.createMultipleDevices(jwt, template_id, 'test', "count=true")
        self.logger.info('Result: ' + str(result))

        #TODO: 'creating devices - Payload must be valid JSON...' (tem como provocar o erro?)

        #TODO: 'creating devices - Missing data for required field ...'

        #TODO:  'a device can not have repeated attributes' (device tem 2 atributos iguais de templates diferentes)

        self.logger.info('creating device - No such template...')
        result = self.createSingleDevice(jwt, 1000, 'dispositivo')
        self.logger.info('Result: ' + str(result))

        #TODO: 'Failed to generate unique device_id' (é erro interno)

        self.logger.info('listing device - No such device...')
        res = self.getDevice(jwt, "123")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing device - internal error...')
        res = self.getDevice(jwt, "abc")
        self.logger.info('Result: ' + str(res))

        self.logger.info('removing specific device - No such device...')
        device_id = 2
        res = self.deleteDevice(jwt, '123')
        self.logger.info('Result: ' + str(res))

        """
        self.logger.info('updating specific device - No such device...')
        res = self.updateDevice(jwt, device_id, template)
        self.logger.info('Result: ' + str(res))
        """

        self.logger.info('listing devices with parameter: page_num=0...')
        res = self.getDevicesWithParameters(jwt, "page_num=0")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing devices with parameter: page_size=0...')
        res = self.getDevicesWithParameters(jwt, "page_size=0")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing devices with parameter: page_size and page_num must be integers...')
        res = self.getDevicesWithParameters(jwt, "page_num=xyz&page_size=kwv")
        self.logger.info('Result: ' + str(res))
