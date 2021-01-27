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

        return rc, res if rc == 400 else None

    def updateTemplate(self, jwt: str, tempĺate_id: int, template: str):
        rc, res = Api.update_template(jwt, tempĺate_id, json.dumps(template))
        #self.assertTrue(isinstance(template_id, int), "Error on update template")
        return rc, res["updated"]["id"] if rc == 200 else res



    def runTest(self):
        self.logger.info('Executing template test')
        self.logger.debug('getting jwt...')
        jwt = Api.get_jwt()

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
                    "value_type": "boolean"
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
                    "label": "bool",
                    "type": "dynamic",
                    "value_type": "boolean"
                },
                {
                    "label": "objeto",
                    "type": "dynamic",
                    "value_type": "object"
                }
            ]
        }



        self.logger.debug('creating template com metadados...')
        template = {
            "label": "Metadado",
            "attrs": [
                {
                    "label": "temperatura",
                    "type": "dynamic",
                    "value_type": "float",
                    "metadata": [{"label": "unidade", "type": "meta", "value_type": "string", "static_value": "°C"}]
                }
            ]
        }

        template_id = self.createTemplate(jwt, template)
        self.logger.info('Template created: '+ str(template_id))


        self.logger.debug('creating template vazio...')
        template = {
            "label": "Vazio",
            "attrs": []
        }

        template_id = self.createTemplate(jwt, template)
        self.logger.info('Template created: '+ str(template_id))


        self.logger.debug('creating template update de firmware...')
        template = {
            "label": "UpdateFW",
            "attrs": []
        }

        template_id = self.createTemplate(jwt, template)
        self.logger.info('Template created: '+ str(template_id))


        self.logger.debug('updating template ......')
        template = {
            "label": "temperatura",
            "attrs": [
                {
                    "label": "temperatura",
                    "type": "dynamic",
                    "value_type": "float",
                    "metadata": [{"label": "unidade", "type": "meta", "value_type": "string", "static_value": "K"}]
                }
                ]
        }

        #template_id = Api.get_templateid_by_label(jwt, 'Metadado')
        template_id = 2
        res = self.updateTemplate(jwt, template_id, template)
        self.logger.info('Template updated: ' + str(res))


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
        self.logger.info('Template is not created:' + str(res))


