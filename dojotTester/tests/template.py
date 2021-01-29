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

    def createTemplateFail(self, jwt: str, template: str):
        rc, res = Api.create_template(jwt, json.dumps(template))

        #return rc, res if rc != 200 else res
        return res

    def updateTemplate(self, jwt: str, tempĺate_id: int, template: str):
        rc, res = Api.update_template(jwt, tempĺate_id, json.dumps(template))
        #self.assertTrue(isinstance(template_id, int), "Error on update template")
        return res if rc == 200 else res

    def getTemplates(self, jwt: str):
        res = Api.get_templates(jwt)
        #self.assertTrue(isinstance(template_id, int), "Error on update template")
        return res

    def getTemplatesWithParameters(self, jwt: str, attrs: str):
        res = Api.get_templates_with_parameters(jwt, attrs)
        # self.assertTrue(isinstance(template_id, int), "Error on update template")
        return res

    def getTemplate(self, jwt: str, template_id: int):
        res = Api.get_template(jwt, template_id)
        #self.assertTrue(isinstance(template_id, int), "Error on update template")
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


        ##FIXME: corrigir get_templateid_by_label para não precisar guardar o template_id
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

        #template_id = Api.get_templateid_by_label(jwt, 'SensorModel')
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
        attrs = {"page_size=5"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: page_num...')
        attrs = {"page_num=2"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: page_size=2&page_num=1...')
        attrs = {"page_size=2&page_num=1"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: page_size=2&page_num=2...')
        attrs = {"page_size=2&page_num=2"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: page_size=2&page_num=3...')
        attrs = {"page_size=2&page_num=3"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: ?page_size=2&page_num=4...')
        attrs = {"page_size=2&page_num=4"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: attr_format=both...')  #both: attrs + data_attrs
        attrs = {"attr_format=both"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: attr_format=single...')  #single: só attrs
        attrs = {"attr_format=single"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: attr_format=split...')  #split: só data_attrs
        attrs = {"attr_format=split"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: attr...')  #só é válido para atributos estáticos
        attrs = {"attr=serial=indefinido"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: label...')
        attrs = {"label=SensorModel"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameter: sortBy...')
        attrs = {"sortBy=label"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameters...')
        attrs = {"page_size=2&page_num=1&attr_format=single&attr=serial=indefinido&label=TiposAtributos&sortBy=label"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameters (no match): return empty...')
        attrs = {"page_size=2&page_num=1&attr_format=single&attr=serial=indefinido&label=SensorModel&sortBy=label"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))

        self.logger.info('listing templates with parameters - internal error...')
        attrs = {"/sortBy=label"}
        res = self.getTemplatesWithParameters(jwt, attrs)
        self.logger.debug('Templates: ' + str(res))


        """
        Fluxos Alternativos
        """

        self.logger.debug('creating template sem label...')
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
        self.logger.info(str(res))

        self.logger.debug('creating template com metadado repetido...')
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
        self.logger.info('Template is not created: ' + str(res))
