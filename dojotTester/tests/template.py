from tests.base_test import BaseTest
from dojot.api import DojotAPI as Api
import json
import random
import time


class TemplateTest(BaseTest):

    def createTemplate(self, jwt: str, template: str):
        rc, template_id = Api.create_template(jwt, json.dumps(template))
        self.assertTrue(isinstance(template_id, int), "Error on create template")

        return template_id if rc == 200 else None

    def createTemplateFail(self, jwt: str, template: str):  ##criado para não interferir no resultado do createTemplate, usado no append
        rc, res = Api.create_template(jwt, json.dumps(template))

        #return rc, res if rc != 200 else res
        return res

    def updateTemplate(self, jwt: str, tempĺate_id: int, template: str):
        rc, res = Api.update_template(jwt, tempĺate_id, json.dumps(template))
        #self.assertTrue(isinstance(template_id, int), "Error on update template")
        return res if rc == 200 else res

    def getTemplates(self, jwt: str):
        res = Api.get_templates(jwt)
        #self.assertTrue(isinstance(template_id, int), "Error on get template")
        return res

    def getTemplatesWithParameters(self, jwt: str, attrs: str):
        res = Api.get_templates_with_parameters(jwt, attrs)
        # self.assertTrue(isinstance(template_id, int), "Error on get template")
        return res

    def getTemplate(self, jwt: str, template_id: int):
        res = Api.get_template(jwt, template_id)
        #self.assertTrue(isinstance(template_id, int), "Error on get template")
        return res

    def getTemplateWithParameters(self, jwt: str, template_id: int, attrs: str):
        res = Api.get_template_with_parameters(jwt, template_id, attrs)
        # self.assertTrue(isinstance(template_id, int), "Error on get template")
        return res

    def deleteTemplates(self, jwt: str):
        res = Api.delete_templates(jwt)
        #self.assertTrue(isinstance(template_id, int), "Error on delete template")
        return res

    def deleteTemplate(self, jwt: str, template_id: int):
        res = Api.delete_template(jwt, template_id)
        #self.assertTrue(isinstance(template_id, int), "Error on delete template")
        return res


    def runTest(self):
        self.logger.info('Executing template test')
        self.logger.debug('getting jwt...')
        jwt = Api.get_jwt()

        self.logger.debug('listing all templates...')
        list = self.getTemplates(jwt)
        self.logger.debug('Templates: ' + str(list))

        self.logger.debug('creating template com todos os tipos de atributos...')
        template = {
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
                    "value_type": "geo:point"
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

        template_id = self.createTemplate(jwt, template)
        self.logger.info('Template created: ' + str(template_id) + ', TiposAtributos')


        self.logger.debug('creating template vazio...')
        template = {
            "label": "Vazio",
            "attrs": []
        }

        template_id = self.createTemplate(jwt, template)
        self.logger.info('Template created: ' + str(template_id) + ', Vazio')


        self.logger.debug('creating and updating template ......')
        template = {
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
        }

        template_id2 = self.createTemplate(jwt, template)
        self.logger.info('Template created: ' + str(template_id2) + ', SensorModel')

        self.logger.debug('listing created template...')
        list = self.getTemplate(jwt, template_id2)
        self.logger.debug('Template: ' + str(list))


        self.logger.debug('updating template ......')
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

        #template_id de 'SensorModel')
        rc, res = self.updateTemplate(jwt, template_id2, template)
        self.logger.info('Template updated: ' + str(template_id2) + ', SensorModel')

        self.logger.debug('listing updated template...')
        list = self.getTemplate(jwt, template_id2)
        self.logger.debug('Template: ' + str(list))


        self.logger.debug('creating template com valores estáticos vazios...')
        template = {
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
        }

        res = self.createTemplate(jwt, template)
        self.logger.info('Template created: ' + str(res) + ', valores estaticos vazios')


        self.logger.debug('creating template firmware_update...')
        template = {
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
        }

        template_id = self.createTemplate(jwt, template)
        self.logger.info('Template created: ' + str(template_id) + ', firmware_update')

        #TODO: adicionar imagem (endpoints /image e /binary)

        """
        Lista templates
        """

        self.logger.info('listing all templates...')
        list = self.getTemplates(jwt)
        self.logger.debug('Template List: ' + str(list))

        self.logger.info('listing templates with parameter: page_size...')
        res = self.getTemplatesWithParameters(jwt, "page_size=3")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: page_num...')
        res = self.getTemplatesWithParameters(jwt, "page_num=2")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: page_size=2&page_num=1...')
        res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=1")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: page_size=2&page_num=2...')
        res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=2")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: page_size=2&page_num=3...')
        res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=3")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: page_size=2&page_num=4...')
        res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=4")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: attr_format=both...')  #both: attrs + data_attrs
        res = self.getTemplatesWithParameters(jwt, "attr_format=both")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: attr_format=single...')  #single: só attrs
        res = self.getTemplatesWithParameters(jwt, "attr_format=single")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: attr_format=split...')  #split: só data_attrs
        res = self.getTemplatesWithParameters(jwt, "attr_format=split")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: attr...')  #só é válido para atributos estáticos
        res = self.getTemplatesWithParameters(jwt, "attr=serial=indefinido")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: label...')
        res = self.getTemplatesWithParameters(jwt, "label=SensorModel")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: sortBy...')
        res = self.getTemplatesWithParameters(jwt, "sortBy=label")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameters...')
        res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=1&attr_format=single&attr=serial=indefinido&label=TiposAtributos&sortBy=label")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameters (no match): return empty...')
        res = self.getTemplatesWithParameters(jwt, "page_size=2&page_num=1&attr_format=single&attr=serial=indefinido&label=SensorModel&sortBy=label")
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameters (nonexistent parameter ): return full...')
        res = self.getTemplatesWithParameters(jwt, "parametro=outro")
        self.logger.debug('Templates: ' + str(res))

        """
        Lista template especifico
        """

        self.logger.info('listing specific template...')
        template_id3 = 3 ##template SensorModel
        res = self.getTemplate(jwt, template_id3)
        self.logger.debug('Template info: ' + str(res))

        self.logger.info('listing specific template with parameter: attr_format=both...')  # both: attrs + data_attrs
        res = self.getTemplateWithParameters(jwt, template_id3, "attr_format=both")
        self.logger.debug('Template info: ' + str(res))

        """
        attr_format: issue #1967
        """

        self.logger.info('listing specific template with parameter: attr_format=single...')  # single: só attrs
        res = self.getTemplateWithParameters(jwt, template_id3, "attr_format=single")
        self.logger.debug('Template info: ' + str(res))

        """
        attr_format: issue #1967
        """

        self.logger.info('listing specific template with parameter: attr_format=split...')  # split: só data_attrs
        res = self.getTemplateWithParameters(jwt, template_id3, "attr_format=split")
        self.logger.debug('Template info: ' + str(res))

        """
        Remove template especifico
        """
        template_id = 2  ##precisa criar um device desse template
        self.logger.info('removing specific template - Templates cannot be removed as they are being used by devices...')
        res = self.deleteTemplate(jwt, template_id)
        self.logger.info('Result: ' + str(res))

        self.logger.info('removing specific template...')
        template_id = 17 ##template Vazio, se o Sanity foi executado antes
        res = self.deleteTemplate(jwt, template_id)
        self.logger.info('Result: ' + str(res))

        """
        Remove all templates
        """

        ##só remove se não existir devices

        Api.delete_devices(jwt)

        self.logger.info('removing all templates...')
        res = self.deleteTemplates(jwt)
        self.logger.debug('Result: ' + str(res))


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
        template_id = 2
        res = self.updateTemplate(jwt, template_id, template)
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing template - No such template...')
        res = self.getTemplate(jwt, "123")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing template - internal error...')
        res = self.getTemplate(jwt, "abc")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing templates with parameter: page_num=0...')
        res = self.getTemplatesWithParameters(jwt, "page_num=0")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing templates with parameter: page_size=0...')
        res = self.getTemplatesWithParameters(jwt, "page_size=0")
        self.logger.info('Result: ' + str(res))


        self.logger.info('listing templates with parameter: page_size and page_num must be integers...')
        res = self.getTemplatesWithParameters(jwt, "page_num=xyz&page_size=kwv")
        self.logger.info('Result: ' + str(res))

        self.logger.info('removing specific template - No such template...')
        template_id = 2
        res = self.deleteTemplate(jwt, template_id)
        self.logger.info('Result: ' + str(res))



