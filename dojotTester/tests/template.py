from tests.base_test import BaseTest
from dojot.api import DojotAPI as Api
import json
import random
import time


class TemplateTest(BaseTest):

    """
    Cria templates:
        - TiposAtributos
        - Vazio
        - SensorModel
        - valores estáticos vazios
        - firmware_update
    """


    def createTemplates(self, jwt: str, templates: list):
        template_ids = []
        for template in templates:
            rc, template_id = Api.create_template(jwt, json.dumps(template))
            #self.assertTrue(isinstance(template_id, int), "Error on create template")

            template_ids.append(template_id["template"]["id"]) if rc == 200 else template_ids.append(None)
        return template_ids

    def createDevices(self, jwt: str, devices: list):
        device_ids = []

        for templates, label in devices:
            self.logger.info('adding device ' + label + ' using templates ' + str(templates))
            rc, device_id = Api.create_device(jwt, templates, label)
            self.assertTrue(device_id is not None, "Error on create device")
            device_ids.append(device_id) if rc == 200 else device_ids.append(None)

        return device_ids

    def createTemplateFail(self, jwt: str, template: str):  ##criado para não interferir no resultado do createTemplate, usado no append
        rc, res = Api.create_template(jwt, json.dumps(template))

        #return rc, res if rc != 200 else res
        return rc, res

    def updateTemplate(self, jwt: str, tempĺate_id: int, template: str):
        rc, res = Api.update_template(jwt, tempĺate_id, json.dumps(template))
        #self.assertTrue(isinstance(template_id, int), "Error on update template")
        return rc, res

    def getTemplates(self, jwt: str):
        rc, res = Api.get_templates(jwt)
        #self.assertTrue(isinstance(template_id, int), "Error on get template")
        return rc, res

    def getTemplatesWithParameters(self, jwt: str, attrs: str):
        rc, res = Api.get_templates_with_parameters(jwt, attrs)
        # self.assertTrue(isinstance(template_id, int), "Error on get template")
        return rc, res

    def getTemplate(self, jwt: str, template_id: int):
        rc, res = Api.get_template(jwt, template_id)
        #self.assertTrue(isinstance(template_id, int), "Error on get template")
        return rc, res

    def getTemplateWithParameters(self, jwt: str, template_id: int, attrs: str):
        rc, res = Api.get_template_with_parameters(jwt, template_id, attrs)
        # self.assertTrue(isinstance(template_id, int), "Error on get template")
        return rc, res

    def deleteTemplates(self, jwt: str):
        rc, res = Api.delete_templates(jwt)
        #self.assertTrue(isinstance(template_id, int), "Error on delete template")
        return rc, res

    def deleteTemplate(self, jwt: str, template_id: int):
        rc, res = Api.delete_template(jwt, template_id)
        #self.assertTrue(isinstance(template_id, int), "Error on delete template")
        return rc, res


    def runTest(self):
        self.logger.info('Executing template test')
        self.logger.debug('getting jwt...')
        jwt = Api.get_jwt()

        self.logger.info('listing all templates - no data...')
        rc, res = self.getTemplates(jwt)
        self.logger.debug('Template List: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        templates = []
        self.logger.debug('creating templates...')
        templates.append({
            "label": "TiposAtributos",
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
            "label": "Vazio",
            "attrs": []
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
            "label": "valores estaticos vazios",
            "attrs": [
                {
                    "label": "SerialNumber",
                    "type": "static",
                    "value_type": "string",
                    "static_value": ""
                },
                {
                    "label": "location",
                    "static_value": "",
                    "type": "static",
                    "value_type": "geo:point"
                }
                ]
        })
        templates.append({
            "label": "firmware_update",
            "attrs": [
                {
                    "label": "transferred_version",
                    "type": "actuator",
                    "value_type": "string",
                    "metadata": [
                        {
                            "label": "dojot:firmware_update:desired_version",
                            "type": "static",
                            "value_type": "boolean",
                            "static_value": True
                        },
                        {
                            "label": "path",
                            "type": "lwm2m",
                            "static_value": "/5/0/1",
                            "value_type": "string"
                        }
                    ]
                },
                {
                    "label": "image_state",
                    "type": "dynamic",
                    "value_type": "integer",
                    "metadata": [
                        {
                            "label": "dojot:firmware_update:state",
                            "type": "static",
                            "value_type": "boolean",
                            "static_value": True
                        },
                        {
                            "type": "lwm2m",
                            "label": "path",
                            "static_value": "/5/0/3",
                            "value_type": "string"
                        }
                    ]
                },
                {
                    "label": "update_result",
                    "type": "dynamic",
                    "value_type": "integer",
                    "metadata": [
                        {
                            "label": "dojot:firmware_update:update_result",
                            "type": "static",
                            "value_type": "boolean",
                            "static_value": True
                        },
                        {
                            "type": "lwm2m",
                            "label": "path",
                            "static_value": "/5/0/5",
                            "value_type": "string"
                        }
                    ]
                },
                {
                    "label": "apply_image",
                    "type": "actuator",
                    "value_type": "string",
                    "metadata": [
                        {
                            "label": "dojot:firmware_update:update",
                            "type": "static",
                            "value_type": "boolean",
                            "static_value": True
                        },
                        {
                            "type": "lwm2m",
                            "label": "path",
                            "static_value": "/5/0/2",
                            "value_type": "string"
                        },
                        {
                            "type": "lwm2m",
                            "label": "operations",
                            "static_value": "e",
                            "value_type": "string"
                        }
                    ]
                },
                {
                    "label": "current_version",
                    "type": "dynamic",
                    "value_type": "string",
                    "metadata": [
                        {
                            "label": "dojot:firmware_update:version",
                            "type": "static",
                            "value_type": "boolean",
                            "static_value": True
                        },
                        {
                            "type": "lwm2m",
                            "label": "path",
                            "static_value": "/3/0/3",
                            "value_type": "string"
                        }
                    ]
                }
            ]
        })


        template_ids = self.createTemplates(jwt, templates)
        self.logger.info("templates ids: " + str(template_ids))

        self.logger.debug('updating template SensorModel......')
        template = {
            "label": "SensorModel",
            "attrs": [
                {
                    "label": "led",
                    "type": "dynamic",
                    "value_type": "bool"
                },
                {
                    "label": "fan",
                    "type": "dynamic",
                    "value_type": "bool"
                }
            ]
        }


        self.logger.debug('listing template SensorModel...')
        rc, res = self.getTemplate(jwt, template_ids[2])
        self.logger.debug('Template: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        rc, res = self.updateTemplate(jwt, template_ids[2], template)
        self.logger.info('Template updated: ' + str(template_ids[2]) + ', SensorModel')
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.debug('listing updated template...')
        rc, res = self.getTemplate(jwt, template_ids[2])
        self.logger.debug('Template: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        """
        Lista templates
        """

        self.logger.info('listing all templates...')
        rc, res = self.getTemplates(jwt)
        self.logger.debug('Template List: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: page_size...')
        rc, res = self.getTemplatesWithParameters(jwt, "page_size=3")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: page_num...')
        rc, res = self.getTemplatesWithParameters(jwt, "page_num=2")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: page_size=2&page_num=1...')
        rc, res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=1")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: page_size=2&page_num=2...')
        rc, res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=2")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: page_size=2&page_num=3...')
        rc, res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=3")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: page_size=2&page_num=4...')
        rc, res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=4")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: attr_format=both...')  #both: attrs + data_attrs
        rc, res = self.getTemplatesWithParameters(jwt, "attr_format=both")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: attr_format=single...')  #single: só attrs
        rc, res = self.getTemplatesWithParameters(jwt, "attr_format=single")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: attr_format=split...')  #split: só data_attrs
        rc, res = self.getTemplatesWithParameters(jwt, "attr_format=split")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: attr...')  #só é válido para atributos estáticos
        rc, res = self.getTemplatesWithParameters(jwt, "attr=serial=indefinido")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: label...')
        rc, res = self.getTemplatesWithParameters(jwt, "label=SensorModel")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameter: sortBy...')
        rc, res = self.getTemplatesWithParameters(jwt, "sortBy=label")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameters...')
        rc, res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=1&attr_format=single&attr=serial=indefinido&label=TiposAtributos&sortBy=label")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameters (no match): return empty...')
        rc, res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=1&attr_format=single&attr=serial=indefinido&label=SensorModel&sortBy=label")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing templates with parameters (nonexistent parameter ): return full...')
        rc, res = self.getTemplatesWithParameters(jwt, "parametro=outro")
        self.logger.debug('Templates: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        """
        Lista template especifico
        """

        self.logger.info('listing specific template...' + str(template_ids[2]))
        ##template SensorModel
        rc, res = self.getTemplate(jwt, template_ids[2])
        self.logger.debug('Template info: ' + str(res))
        #self.assertTrue(int(rc) == 200, "codigo inesperado")

        self.logger.info('listing specific template with parameter: attr_format=both...')  # both: attrs + data_attrs
        rc, res = self.getTemplateWithParameters(jwt, template_ids[2], "attr_format=both")
        self.logger.debug('Template info: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        """
        attr_format: issue #1967
        """

        self.logger.info('listing specific template with parameter: attr_format=single...')  # single: só attrs
        rc, res = self.getTemplateWithParameters(jwt, template_ids[2], "attr_format=single")
        self.logger.debug('Template info: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        """
        attr_format: issue #1967
        """

        self.logger.info('listing specific template with parameter: attr_format=split...')  # split: só data_attrs
        rc, res = self.getTemplateWithParameters(jwt, template_ids[2], "attr_format=split")
        self.logger.debug('Template info: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        """
        Remove template especifico
        """

        self.logger.info('removing specific template...')
        ##template Vazio
        rc, res = self.deleteTemplate(jwt, template_ids[1])
        self.logger.debug('Result: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")

        devices = []
        devices.append(([template_ids[2]], "device"))
        devices_ids = self.createDevices(jwt, devices)
        self.logger.info("devices ids: " + str(devices_ids))

        self.logger.info('removing specific template - Templates cannot be removed as they are being used by devices...')
        rc, res = self.deleteTemplate(jwt, template_ids[2])
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 400, "codigo inesperado")
        self.assertTrue(res["message"] == "Templates cannot be removed as they are being used by devices", "mensagem inesperada")


        """
        Remove all templates
        """

        ##só remove se não existir devices associados

        Api.delete_devices(jwt)
        """

        self.logger.info('removing all templates...')
        rc, res = self.deleteTemplates(jwt)
        self.logger.debug('Result: ' + str(res))
        self.assertTrue(int(rc) == 200, "codigo inesperado")
        """


        """
        Fluxos Alternativos
        """

        self.logger.info('creating template sem label...')
        template = {
            "attrs": [
                {
                    "label": "float",
                    "type": "dynamic",
                    "value_type": "float"
                }
                ]
        }

        res = self.createTemplateFail(jwt, template)
        self.logger.info('Result: ' + str(res))


        self.logger.info('creating template com metadado repetido...')
        template = {
            "label": "sample",
            "attrs": [
                {
                    "label": "simpleAttr",
                    "type": "dynamic",
                    "value_type": "string",
                    "metadata": [
                        {"type": "mapping", "label": "type2", "static_value": "dummy", "value_type": "string"},
                        {"type": "mapping", "label": "type2", "static_value": "dummy", "value_type": "string"}
                    ]
                }
            ]
        }

        res = self.createTemplateFail(jwt, template)
        self.logger.info('Result: ' + str(res))

        self.logger.info('updating specific template - No such template...')
        template = {
            "label": "Vazio",
            "attrs": [
                {
                    "label": "serial",
                    "type": "static",
                    "value_type": "string",
                    "static_value": "undefined"
                }
            ]
        }
        rc, res = self.updateTemplate(jwt, 1000, template)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 404, "codigo inesperado")

        self.logger.info('listing template - No such template...')
        rc, res = self.getTemplate(jwt, "123")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 404, "codigo inesperado")

        self.logger.info('listing template - internal error...')
        rc, res = self.getTemplate(jwt, "abc")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 500, "codigo inesperado")

        self.logger.info('listing templates with parameter: page_num=0...')
        rc, res = self.getTemplatesWithParameters(jwt, "page_num=0")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 400, "codigo inesperado")

        self.logger.info('listing templates with parameter: page_size=0...')
        res = self.getTemplatesWithParameters(jwt, "page_size=0")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 400, "codigo inesperado")

        self.logger.info('listing templates with parameter: page_size and page_num must be integers...')
        rc, res = self.getTemplatesWithParameters(jwt, "page_num=xyz&page_size=kwv")
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 500, "codigo inesperado")

        self.logger.info('removing specific template - No such template...')
        rc, res = self.deleteTemplate(jwt, 1000)
        self.logger.info('Result: ' + str(res))
        self.assertTrue(int(rc) == 404, "codigo inesperado")

