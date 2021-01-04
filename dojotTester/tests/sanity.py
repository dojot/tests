from tests.base_test import BaseTest
from dojot.api import DojotAPI as Api
from mqtt.mqttClient import MQTTClient
import json
import random
import time

class SanityTest(BaseTest):
    """
    Cria templates:
        - medidor de temperatura
        - medidor de pressao
        - medidor de umidade relativa
        - medidor de velocidade
        - protocolo
        - onibus
        - controladores
        - TesteTemplate
        - CameraTemplate
        - MedidorChuva
        - MedidorNivel
        - logger
        - CameraTemplateQualcomm
        - ObterAcesso
        - Token
    """
    def createTemplates(self, jwt: str, templates: list):
        template_ids = []
        for template in templates:
            rc, template_id = Api.create_template(jwt, json.dumps(template))
            self.assertTrue(isinstance(template_id, int), "Error on create template")

            template_ids.append(template_id) if rc == 200 else template_ids.append(None)
        return template_ids

    def createDevices(self, jwt: str, devices: list):
        device_ids = []

        for templates, label in devices:
            self.logger.info('adding device ' + label + ' using templates ' + str(templates))
            rc, device_id = Api.create_device(jwt, templates, label)
            self.assertTrue(device_id is not None, "Error on create device")
            device_ids.append(device_id) if rc == 200 else device_ids.append(None)

        return device_ids

    def createFlows(self, jwt: str, flows: list):
        flows_ids = []

        for flow in flows:
            self.logger.info('adding flow..')
            rc, flow_id = Api.create_flow(jwt, flow)
            self.assertTrue(flow_id is not None, "Error on create flow")
            flows_ids.append(flow_id) if rc == 200 else flows_ids.append(None)

        return flows_ids

    def runTest(self):
        self.logger.info('Executing sanity test')
        self.logger.debug('getting jwt...')
        jwt = Api.get_jwt()

        templates = []
        self.logger.debug('creating templates...')
        templates.append({
            "label": "medidor de temperatura",
            "attrs": [
                {
                    "label": "temperatura",
                    "type": "dynamic",
                    "value_type": "float",
                    "metadata": [{"label": "unidade", "type": "meta", "value_type": "string", "static_value": "°C"}]
                }
            ]
        }
        )
        templates.append({
            "label": "medidor de pressao",
            "attrs": [
                {
                    "label": "SerialNumber",
                    "type": "static",
                    "value_type": "string",
                    "static_value": "undefined"
                },
                {
                    "label": "pressao",
                    "type": "dynamic",
                    "value_type": "float",
                    "metadata": [{"label": "unidade", "type": "meta", "value_type": "string", "static_value": "mmHg"}]
                }
            ]
        })
        templates.append({
            "label": "medidor de umidade relativa",
            "attrs": [
                {
                    "label": "umidade",
                    "type": "dynamic",
                    "value_type": "float",
                    "metadata": [{"label": "unidade", "type": "meta", "value_type": "string", "static_value": "%"}]
                }
            ]
        })
        templates.append({
            "label": "medidor de velocidade",
            "attrs": [
                {
                    "label": "velocidade",
                    "type": "dynamic",
                    "value_type": "float",
                    "metadata": [{"label": "unidade", "type": "meta", "value_type": "string", "static_value": "km/h"}]
                }
            ]
        })
        templates.append({
            "label": "protocolo",
            "attrs": [
                {
                    "label": "protocol",
                    "static_value": "mqtt",
                    "type": "static",
                    "value_type": "string"
                }
            ]
        })
        templates.append({
            "label": "onibus",
            "attrs": [
                {
                    "label": "velocidade",
                    "metadata": [
                        {"label": "unidade", "type": "meta", "value_type": "string", "static_value": "km/h"}],
                    "type": "dynamic",
                    "value_type": "float"
                },
                {
                    "label": "passageiros",
                    "type": "dynamic",
                    "value_type": "integer"
                },
                {
                    "label": "carro",
                    "type": "static",
                    "value_type" : "string",
                    "static_value" : "indefinido"
                },
                {
                    "label": "gps",
                    "type": "dynamic",
                    "value_type": "geo:point"
                },
                {
                    "label": "operacional",
                    "type": "dynamic",
                    "value_type": "boolean"
                },
                {
                    "label": "mensagem",
                    "type": "dynamic",
                    "value_type" : "string"
                },
                {
                    "label": "protocol",
                    "static_value": "mqtt",
                    "type": "static",
                    "value_type": "string"
                },
                {
                    "label": "device_timeout",
                    "static_value": "10000",
                    "type": "static",
                    "value_type": "string"
                },
                {
                    "label": "letreiro",
                    "static_value": "",
                    "type": "actuator",
                    "value_type": "string"
                }
            ]
        })
        templates.append({
            "label": "controladores",
            "attrs": [
                {
                    "label": "mensagem",
                    "type": "dynamic",
                    "value_type": "string"
                },
                {
                    "label": "medida",
                    "type": "dynamic",
                    "value_type": "float"
                },
                {
                    "label": "display",
                    "static_value": "",
                    "type": "actuator",
                    "value_type": "string"
                },
                {
                    "label": "objeto",
                    "static_value": "",
                    "type": "actuator",
                    "value_type": "object"
                }
            ]
        })
        templates.append({
            "label": "TesteTemplate",
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
                    "label": "str",
                    "type": "dynamic",
                    "value_type" : "string"
                },
                {
                    "label": "gps",
                    "type": "dynamic",
                    "value_type": "geo:point",
                    "metadata": [
                        {"label": "unidade", "type": "meta", "value_type": "string", "static_value": "decimal"},
                        {"label": "descricao", "type": "meta", "value_type": "string", "static_value": "localização do dispositivo"}
                    ]
                },
                {
                    "label": "bool",
                    "type": "dynamic",
                    "value_type": "boolean"
                },
                {
                    "label": "serial",
                    "type": "static",
                    "value_type" : "string",
                    "static_value" : "indefinido"
                },
                {
                    "label": "mensagem",
                    "static_value": "",
                    "type": "actuator",
                    "value_type": "string"
                },
                {
                    "label": "protocol",
                    "static_value": "mqtt",
                    "type": "static",
                    "value_type": "string"
                }
            ]
        })
        templates.append({
            "label": "CameraTemplate",
            "attrs": [
                {"label":"license_plate","type":"dynamic","value_type":"string"},
                {"label":"band","type":"dynamic","value_type":"integer"},
                {"label":"coordinates","type":"dynamic","value_type":"string"},
                {"label":"vehicle_type","type":"dynamic","value_type":"string"},
                {"label":"timestamp","type":"dynamic","value_type":"integer"}
            ]
        })
        templates.append({
            "label": "MedidorChuva",
            "attrs": [
                {
                    "label": "chuva",
                    "type": "dynamic",
                    "value_type": "float"
                }
            ]
        })
        templates.append({
            "label": "MedidorNivel",
            "attrs": [
                {
                    "label": "nivel",
                    "type": "dynamic",
                    "value_type": "float"
                }
            ]
        })
        templates.append({
            "label": "logger",
            "attrs": [
                {
                    "label": "data",
                    "type": "dynamic",
                    "value_type": "object"
                },
                {
                    "label": "metadata",
                    "type": "dynamic",
                    "value_type": "object"
                }
            ]
        })
        templates.append({
            "label": "ObterAcesso",
            "attrs": [
                {
                    "label": "username",
                    "type": "dynamic",
                    "value_type": "string"
                },
                {
                    "label": "passwd",
                    "type": "dynamic",
                    "value_type": "string"
                }
            ]
        })
        templates.append({
            "label": "Token",
            "attrs": [
                {
                    "label": "json",
                    "type": "dynamic",
                    "value_type": "object"
                },
                {
                    "label": "jwt",
                    "type": "dynamic",
                    "value_type": "string"
                }
            ]
        })
        templates.append({
            "label": "CameraTemplateQualcomm",
            "attrs": [
                {"label":"license_plate","type":"dynamic","value_type":"string"},
                {"label":"band","type":"dynamic","value_type":"integer"},
                {"label":"coordinates","type":"dynamic","value_type":"geo:point"},
                {"label":"vehicle_type","type":"dynamic","value_type":"string"},
                {"label":"timestamp","type":"dynamic","value_type":"integer"}
            ]
        })

        template_ids = self.createTemplates(jwt, templates)
        self.logger.info("templates ids: " + str(template_ids))

        devices = []
        devices.append(([template_ids[0], template_ids[4]], "termometro"))
        devices.append(([template_ids[0], template_ids[4]], "termometro kelvin"))
        devices.append(([template_ids[1], template_ids[4]], "barometro"))
        devices.append(([template_ids[2], template_ids[4]], "higrometro"))
        devices.append(([template_ids[3], template_ids[4]], "anemometro"))
        devices.append(([template_ids[0], template_ids[1], template_ids[2], template_ids[3]], "instrumento de medicao"))
        devices.append(([template_ids[5]], "linha_1"))
        devices.append(([template_ids[5]], "linha_2"))
        devices.append(([template_ids[5]], "linha_3"))
        devices.append(([template_ids[6]], "controle"))
        devices.append(([template_ids[7]], "device"))
        devices.append(([template_ids[7]], "dispositivo"))
        devices.append(([template_ids[8]], "Camera1"))
        devices.append(([template_ids[9]], "Pluviometro"))
        devices.append(([template_ids[10]], "SensorNivel"))
        devices.append(([template_ids[11]], "logger"))
        devices.append(([template_ids[12]], "CameraQualcomm"))
        devices.append(([template_ids[13]], "acesso"))
        devices.append(([template_ids[14]], "token"))

        devices_ids = self.createDevices(jwt, devices)
        self.logger.info("devices ids: " + str(devices_ids))

        ###################
        #Configuring flows
        ###################
        flows = []
        flows.append({
            "name": "basic flow",
            "flow": [
                {
                    "id": "38b9fd8d.9d0a72",
                    "type": "tab",
                    "label": "Flow 1"
                },
                {
                    "id": "15bcb272.91022e",
                    "name": "anemometro",
                    "device_source_id": "anemometro " + Api.get_deviceid_by_label(jwt, "anemometro"),
                    "status": "false",
                    "type": "device in",
                    "wires": [["8d24f81d.b96308"]],
                    "x": 205.72567749023438,
                    "y": 214.06947326660156,
                    "z": "38b9fd8d.9d0a72",
                    "_device_id": Api.get_deviceid_by_label(jwt, "anemometro"),
                    "_device_label": "",
                    "_device_type": ""
                },
                {
                    "checkall": "true",
                    "id": "8d24f81d.b96308",
                    "name": "velocidade >= 50",
                    "outputs": 1,
                    "property": "payload.velocidade",
                    "propertyType": "msg",
                    "rules": [{"t": "gte", "v": "50", "vt": "num"}],
                    "type": "switch",
                    "wires": [["9ae043f5.e5d12"]],
                    "x": 346.7292022705078,
                    "y": 285.10418224334717,
                    "z": "38b9fd8d.9d0a72"
                },
                {
                    "action": "",
                    "from": "",
                    "id": "9ae043f5.e5d12",
                    "name": "",
                    "property": "",
                    "reg": "false",
                    "rules": [{"t": "set", "p": "saida.mensagem", "pt": "msg", "to": "vento muito forte", "tot": "str"}],
                    "to": "",
                    "type": "change",
                    "wires": [["62a3753b.7edc0c"]],
                    "x": 502.7291717529297,
                    "y": 361.1180591583252,
                    "z": "38b9fd8d.9d0a72"
                },
                {
                    "attrs": "saida",
                    "device_source": "configured",
                    "devices_source_dynamic": "",
                    "devices_source_dynamicFieldType": "msg",
                    "devices_source_configured": [Api.get_deviceid_by_label(jwt, "controle")],
                    "_devices_loaded": True,
                    "id": "62a3753b.7edc0c",
                    "name": "controle",
                    "type": "multi device out",
                    "wires": [],
                    "x": 688.7326736450195,
                    "y": 435.0903205871582,
                    "z": "38b9fd8d.9d0a72"
                }
            ]
        })
        flows.append({
            "name": "geofence flow",
            "flow":
                [ { "id": "3433da79.e543a6", "type": "tab", "label": "Flow 1" },
                  { "id": "5f77d972.391e98",
                    "type": "event template in",
                    "z": "3433da79.e543a6",
                    "name": "ônibus",
                    "event_create": False,
                    "event_update": False,
                    "event_remove": False,
                    "event_configure": False,
                    "event_publish": True,
                    "template_id": str(template_ids[5]),
                    "x": 359.5,
                    "y": 202,
                    "wires": [ [ "845deaaf.f8cb98", "44c99e4.76b8a6" ] ] },
                  { "id": "845deaaf.f8cb98",
                    "type": "geofence",
                    "z": "3433da79.e543a6",
                    "name": "",
                    "mode": "polyline",
                    "filter": "inside",
                    "points":
                        [ { "latitude": "-22.893729786643423",
                            "longitude": "-47.060708999633796" },
                          { "latitude": "-22.888827380892344", "longitude": "-47.0570182800293" },
                          { "latitude": "-22.887720361534203",
                            "longitude": "-47.053241729736335" },
                          { "latitude": "-22.88724592190222", "longitude": "-47.04869270324708" },
                          { "latitude": "-22.88692962789286", "longitude": "-47.04483032226563" },
                          { "latitude": "-22.890646035948535", "longitude": "-47.04671859741211" },
                          { "latitude": "-22.895073963731004",
                            "longitude": "-47.047061920166016" },
                          { "latitude": "-22.90013427567171", "longitude": "-47.048091888427734" },
                          { "latitude": "-22.905589713001355", "longitude": "-47.0463752746582" },
                          { "latitude": "-22.905115335858504",
                            "longitude": "-47.050237655639656" },
                          { "latitude": "-22.905115335858504", "longitude": "-47.05195426940918" },
                          { "latitude": "-22.906143150903915", "longitude": "-47.05530166625977" },
                          { "latitude": "-22.902427167370448",
                            "longitude": "-47.057275772094734" },
                          { "latitude": "-22.899027348564793",
                            "longitude": "-47.058563232421875" },
                          { "latitude": "-22.896813467251835", "longitude": "-47.05890655517578" } ],
                    "geopoint": "payload.data.attrs.gps",
                    "x": 553.5,
                    "y": 196,
                    "wires": [ [ "d905b5c9.4958e8" ] ] },
                  { "id": "d905b5c9.4958e8",
                    "type": "change",
                    "z": "3433da79.e543a6",
                    "name": "",
                    "rules":
                        [ { "t": "set",
                            "p": "saida.mensagem",
                            "pt": "msg",
                            "to": "Está no Cambuí",
                            "tot": "str" } ],
                    "action": "",
                    "property": "",
                    "from": "",
                    "to": "",
                    "reg": "false",
                    "x": 748.5,
                    "y": 200,
                    "wires": [ [ "25c1c361.88827c" ] ] },
                  { "id": "44c99e4.76b8a6",
                    "type": "geofence",
                    "z": "3433da79.e543a6",
                    "name": "",
                    "mode": "polyline",
                    "filter": "outside",
                    "points":
                        [ { "latitude": "-22.893729786643423",
                            "longitude": "-47.060708999633796" },
                          { "latitude": "-22.888827380892344", "longitude": "-47.0570182800293" },
                          { "latitude": "-22.887720361534203",
                            "longitude": "-47.053241729736335" },
                          { "latitude": "-22.88724592190222", "longitude": "-47.04869270324708" },
                          { "latitude": "-22.88692962789286", "longitude": "-47.04483032226563" },
                          { "latitude": "-22.890646035948535", "longitude": "-47.04671859741211" },
                          { "latitude": "-22.895073963731004",
                            "longitude": "-47.047061920166016" },
                          { "latitude": "-22.90013427567171", "longitude": "-47.048091888427734" },
                          { "latitude": "-22.905589713001355", "longitude": "-47.0463752746582" },
                          { "latitude": "-22.905115335858504",
                            "longitude": "-47.050237655639656" },
                          { "latitude": "-22.905115335858504", "longitude": "-47.05195426940918" },
                          { "latitude": "-22.906143150903915", "longitude": "-47.05530166625977" },
                          { "latitude": "-22.902427167370448",
                            "longitude": "-47.057275772094734" },
                          { "latitude": "-22.899027348564793",
                            "longitude": "-47.058563232421875" },
                          { "latitude": "-22.896813467251835", "longitude": "-47.05890655517578" } ],
                    "geopoint": "payload.data.attrs.gps",
                    "x": 568,
                    "y": 321,
                    "wires": [ [ "44d30981.231c48" ] ] },
                  { "id": "44d30981.231c48",
                    "type": "change",
                    "z": "3433da79.e543a6",
                    "name": "",
                    "rules":
                        [ { "t": "set",
                            "p": "saida.mensagem",
                            "pt": "msg",
                            "to": "Não está no Cambuí",
                            "tot": "str" } ],
                    "action": "",
                    "property": "",
                    "from": "",
                    "to": "",
                    "reg": "false",
                    "x": 773,
                    "y": 320,
                    "wires": [ [ "25c1c361.88827c" ] ] },
                  { "id": "25c1c361.88827c",
                    "type": "multi device out",
                    "z": "3433da79.e543a6",
                    "name": "",
                    "device_source": "self",
                    "devices_source_dynamic": "",
                    "devices_source_dynamicFieldType": "msg",
                    "devices_source_configured": [ "" ],
                    "_devices_loaded": "true",
                    "attrs": "saida",
                    "x": 964.5,
                    "y": 245,
                    "wires": [] }
                  ]
        })
        flows.append({
            "name": "http - POST",
            "flow": [
                { "id": "f66d93e3.8f42e", "type": "tab", "label": "Flow 1" },
                { "id": "853a54b9.f53208",
                  "type": "device template in",
                  "z": "f66d93e3.8f42e",
                  "name": "ônibus",
                  "device_template": { "id": template_ids[5] },
                  "status": "false",
                  "device_template_id": template_ids[5],
                  "x": 136.5,
                  "y": 144,
                  "wires": [ [ "ce40a438.e567c8" ] ] },
                { "id": "784cd62a.09b088",
                  "type": "http",
                  "z": "f66d93e3.8f42e",
                  "name": "",
                  "method": "POST",
                  "ret": "txt",
                  "body": "reqBody",
                  "response": "responseGet",
                  "url": "http://ptsv2.com/t/3fbhu-1543424220/post",
                  "x": 918.5,
                  "y": 408,
                  "wires": [] },
                { "id": "ce40a438.e567c8",
                  "type": "switch",
                  "z": "f66d93e3.8f42e",
                  "name": "velocidade >= 50",
                  "property": "payload.velocidade",
                  "propertyType": "msg",
                  "rules": [ { "t": "gte", "v": "50", "vt": "num" } ],
                  "checkall": "true",
                  "outputs": "1",
                  "x": 409.5,
                  "y": 210,
                  "wires": [ [ "5d51ecfa.baa4e4" ] ] },
                { "id": "5d51ecfa.baa4e4",
                  "type": "template",
                  "z": "f66d93e3.8f42e",
                  "name": "",
                  "field": "reqBody",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{\"payload\": \"velocidade muito alta: {{payload.velocidade}} km/h!\"}",
                  "output": "str",
                  "x": 651.5,
                  "y": 318,
                  "wires": [ [ "784cd62a.09b088" ] ] }
            ]
        })
        flows.append(
            {
                "name": "template e actuate - deprecated nodes",
                "flow":
                    [{"id": "817b663.3500a98", "type": "tab", "label": "Flow 1"},
                     {"id": "eb02c267.272c7",
                      "type": "device template in",
                      "z": "817b663.3500a98",
                      "name": "medidor de umidade",
                      "device_template": {"id": template_ids[2]},
                      "status": "false",
                      "device_template_id": template_ids[2],
                      "x": 122.5,
                      "y": 109,
                      "wires": [["2f581bba.db5e94"]]},
                     {"id": "2f581bba.db5e94",
                      "type": "switch",
                      "z": "817b663.3500a98",
                      "name": "umidade <= 20",
                      "property": "payload.umidade",
                      "propertyType": "msg",
                      "rules": [{"t": "lte", "v": "20", "vt": "num"}],
                      "checkall": "true",
                      "outputs": "1",
                      "x": 346.5,
                      "y": 196,
                      "wires": [["f9d39ec2.e5e26"]]},
                     {"id": "f9d39ec2.e5e26",
                      "type": "template",
                      "z": "817b663.3500a98",
                      "name": "",
                      "field": "saida.mensagem",
                      "fieldType": "msg",
                      "syntax": "handlebars",
                      "template": "baixa umidade relativa do ar: {{payload.umidade}} !",
                      "output": "str",
                      "x": 569.5,
                      "y": 292,
                      "wires": [["35dab849.9344d8"]]},
                     {"id": "35dab849.9344d8",
                      "type": "actuate",
                      "z": "817b663.3500a98",
                      "name": "device",
                      "device_source": "configured",
                      "device_source_msg": "",
                      "device_source_id": "device (" + Api.get_deviceid_by_label(jwt, 'device') + ")",
                      "attrs": "saida",
                      "_device_id": Api.get_deviceid_by_label(jwt, 'device'),
                      "x": 695.5,
                      "y": 393,
                      "wires": []}
                     ]}
        )
        flows.append(
            {
                "name": "email flow",
                "flow":
                    [{"id": "7589258f.32474c", "type": "tab", "label": "Flow 1"},
                     {"id": "443c695c.5f0258",
                      "type": "device template in",
                      "z": "7589258f.32474c",
                      "name": "medidor de temperatura",
                      "device_template": {"id": template_ids[0]},
                      "status": "false",
                      "device_template_id": template_ids[0],
                      "x": 227.5,
                      "y": 130,
                      "wires": [["e332b8ea.277ec8"]]},
                     {"id": "54771336.9f930c",
                      "type": "email",
                      "z": "7589258f.32474c",
                      "server": "gmail-smtp-in.l.google.com",
                      "port": "25",
                      "secure": "false",
                      "name": "",
                      "dname": "",
                      "to": "efaber@cpqd.com.br",
                      "from": "dojotcpqd@gmail.com",
                      "subject": "aviso",
                      "body": "emailBody",
                      "userid": "",
                      "password": "",
                      "x": 880.5,
                      "y": 442,
                      "wires": []},
                     {"id": "e332b8ea.277ec8",
                      "type": "switch",
                      "z": "7589258f.32474c",
                      "name": "temperatura >= 30",
                      "property": "payload.temperatura",
                      "propertyType": "msg",
                      "rules": [{"t": "gte", "v": "30", "vt": "num"}],
                      "checkall": "true",
                      "outputs": "1",
                      "x": 435.5,
                      "y": 225,
                      "wires": [["e853395f.05b6c8"]]},
                     {"id": "e853395f.05b6c8",
                      "type": "template",
                      "z": "7589258f.32474c",
                      "name": "",
                      "field": "emailBody",
                      "fieldType": "msg",
                      "syntax": "handlebars",
                      "template": "Temperatura muito alta: {{payload.temperatura}} °C !",
                      "output": "str",
                      "x": 640.5,
                      "y": 321,
                      "wires": [["54771336.9f930c"]]}
                     ]
            }
        )
        flows.append(
            {
                "name": "aggregation flow",
                "flow":
                    [{"id": "98435f56.9245", "type": "tab", "label": "Flow 1"},
                     {"id": "88edde.0161522",
                      "type": "device in",
                      "z": "98435f56.9245",
                      "name": "anemometro",
                      "device_source_id": "anemometro (" + Api.get_deviceid_by_label(jwt, 'anemometro') + ")",
                      "status": "false",
                      "_device_id": Api.get_deviceid_by_label(jwt, 'anemometro'),
                      "_device_label": "",
                      "_device_type": "",
                      "x": 243.5,
                      "y": 111,
                      "wires": [["377408a3.9807d8"]]},
                     {"id": "27520e8e.5e66e2",
                      "type": "device in",
                      "z": "98435f56.9245",
                      "name": "barometro",
                      "device_source_id": "barometro (" + Api.get_deviceid_by_label(jwt, 'barometro') + ")",
                      "status": "false",
                      "_device_id": Api.get_deviceid_by_label(jwt, 'barometro'),
                      "_device_label": "",
                      "_device_type": "",
                      "x": 236.5,
                      "y": 203,
                      "wires": [["51915a08.9c5114"]]},
                     {"id": "fb20a30f.55923",
                      "type": "device in",
                      "z": "98435f56.9245",
                      "name": "higrometro",
                      "device_source_id": "higrometro (" + Api.get_deviceid_by_label(jwt, 'higrometro') + ")",
                      "status": "false",
                      "_device_id": Api.get_deviceid_by_label(jwt, 'higrometro'),
                      "_device_label": "",
                      "_device_type": "",
                      "x": 247.5,
                      "y": 304,
                      "wires": [["75604141.97a9c"]]},
                     {"id": "2161ad27.fecae2",
                      "type": "device in",
                      "z": "98435f56.9245",
                      "name": "termometro",
                      "device_source_id": "termometro (" + Api.get_deviceid_by_label(jwt, 'termometro') + ")",
                      "status": "false",
                      "_device_id": Api.get_deviceid_by_label(jwt, 'termometro'),
                      "_device_label": "",
                      "_device_type": "",
                      "x": 251.5,
                      "y": 423,
                      "wires": [["afd596e6.3c6ac8"]]},
                     {"id": "377408a3.9807d8",
                      "type": "change",
                      "z": "98435f56.9245",
                      "name": "",
                      "rules":
                          [{"t": "set",
                            "p": "saida.velocidade",
                            "pt": "msg",
                            "to": "payload.velocidade",
                            "tot": "msg"}],
                      "action": "",
                      "property": "",
                      "from": "",
                      "to": "",
                      "reg": "false",
                      "x": 582.5,
                      "y": 111,
                      "wires": [["986ce39c.97953"]]},
                     {"id": "51915a08.9c5114",
                      "type": "change",
                      "z": "98435f56.9245",
                      "name": "",
                      "rules":
                          [{"t": "set",
                            "p": "saida.pressao",
                            "pt": "msg",
                            "to": "payload.pressao",
                            "tot": "msg"}],
                      "action": "",
                      "property": "",
                      "from": "",
                      "to": "",
                      "reg": "false",
                      "x": 600,
                      "y": 186,
                      "wires": [["986ce39c.97953"]]},
                     {"id": "75604141.97a9c",
                      "type": "change",
                      "z": "98435f56.9245",
                      "name": "",
                      "rules":
                          [{"t": "set",
                            "p": "saida.umidade",
                            "pt": "msg",
                            "to": "payload.umidade",
                            "tot": "msg"}],
                      "action": "",
                      "property": "",
                      "from": "",
                      "to": "",
                      "reg": "false",
                      "x": 585,
                      "y": 304,
                      "wires": [["986ce39c.97953"]]},
                     {"id": "afd596e6.3c6ac8",
                      "type": "change",
                      "z": "98435f56.9245",
                      "name": "",
                      "rules":
                          [{"t": "set",
                            "p": "saida.temperatura",
                            "pt": "msg",
                            "to": "payload.temperatura",
                            "tot": "msg"}],
                      "action": "",
                      "property": "",
                      "from": "",
                      "to": "",
                      "reg": "false",
                      "x": 596,
                      "y": 424,
                      "wires": [["986ce39c.97953"]]},
                     {"id": "986ce39c.97953",
                      "type": "multi device out",
                      "z": "98435f56.9245",
                      "name": "instrumento de medicao",
                      "device_source": "configured",
                      "devices_source_dynamic": "",
                      "devices_source_dynamicFieldType": "msg",
                      "devices_source_configured": [Api.get_deviceid_by_label(jwt, 'instrumento de medicao')],
                      "_devices_loaded": True,
                      "attrs": "saida",
                      "x": 950.5,
                      "y": 296,
                      "wires": []}
                     ]
            }
        )

        #TODO Parei no adicionar o no remoto kelvin - adicionar outros fluxos
        ##
        flows_ids = self.createFlows(jwt, flows)

        self.logger.info("Flows created. IDs: " + str(flows_ids))

        group1 = {"name": "viewer" + str(random.randint(0, 100)),
                  "description": "Grupo com acesso somente para visualizar as informações"}
        group1_id = Api.create_group(jwt, group1)

        #TODO adicionar as permissoes ao grupo
        #TODO adicionar usuario
        #TODO listar tenants

        dev1_id = Api.get_deviceid_by_label(jwt, "linha_1")
        dev1_topic = "admin:" + dev1_id + "/attrs"
        dev1 = MQTTClient(dev1_id)
        self.logger.info("publicando com dispositivo: " + dev1_id)
        dev1.publish(dev1_topic,
                     {"gps":"-22.890970, -47.063006","velocidade":50,"passageiros":30,"operacional":False})
        time.sleep(1)
        dev1.publish(dev1_topic,
                     {"gps":"-22.893619, -47.052921","velocidade":40,"passageiros":45,"operacional":True})
        time.sleep(5)

        dev2_id = Api.get_deviceid_by_label(jwt, "dispositivo")
        dev2_topic = "admin:" + dev2_id + "/attrs"
        dev2 = MQTTClient(dev2_id)
        self.logger.info("publicando com dispositivo: " + dev2_id)
        dev2.publish(dev2_topic, {"int": 2})

