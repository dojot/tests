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

            template_ids.append(
                template_id["template"]["id"]) if rc == 200 else template_ids.append(None)
        return template_ids

    def createDevices(self, jwt: str, devices: list):
        device_ids = []

        for templates, label in devices:
            self.logger.info('adding device ' + label +
                             ' using templates ' + str(templates))
            rc, device_id = Api.create_device(jwt, templates, label)
            self.assertTrue(device_id is not None, "Error on create device")
            device_ids.append(
                device_id) if rc == 200 else device_ids.append(None)

        return device_ids

    def createFlows(self, jwt: str, flows: list):
        flows_ids = []

        for flow in flows:
            self.logger.info('adding flow..')
            rc, flow_id = Api.create_flow(jwt, flow)
            self.assertTrue(flow_id is not None, "Error on create flow")
            flows_ids.append(flow_id["flow"]["id"]
                             ) if rc == 200 else flows_ids.append(None)

        return flows_ids

    # def createUsers(self, jwt: str, user: str):

        # Api.create_user(jwt, user)

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
                    "value_type": "string",
                    "static_value": "indefinido"
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
                    "value_type": "string"
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
                    "value_type": "string"
                },
                {
                    "label": "gps",
                    "type": "dynamic",
                    "value_type": "geo:point",
                    "metadata": [
                        {"label": "unidade", "type": "meta",
                            "value_type": "string", "static_value": "decimal"},
                        {"label": "descricao", "type": "meta", "value_type": "string",
                            "static_value": "localização do dispositivo"}
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
                    "value_type": "string",
                    "static_value": "indefinido"
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
                {"label": "license_plate", "type": "dynamic", "value_type": "string"},
                {"label": "band", "type": "dynamic", "value_type": "integer"},
                {"label": "coordinates", "type": "dynamic", "value_type": "string"},
                {"label": "vehicle_type", "type": "dynamic", "value_type": "string"},
                {"label": "timestamp", "type": "dynamic", "value_type": "integer"}
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
                {"label": "license_plate", "type": "dynamic", "value_type": "string"},
                {"label": "band", "type": "dynamic", "value_type": "integer"},
                {"label": "coordinates", "type": "dynamic",
                    "value_type": "geo:point"},
                {"label": "vehicle_type", "type": "dynamic", "value_type": "string"},
                {"label": "timestamp", "type": "dynamic", "value_type": "integer"}
            ]
        })

        template_ids = self.createTemplates(jwt, templates)
        self.logger.info("templates ids: " + str(template_ids))

        devices = []
        devices.append(
            ([template_ids[0], template_ids[4]], "termometro Celsius"))
        devices.append(
            ([template_ids[0], template_ids[4]], "termometro Kelvin"))
        devices.append(([template_ids[1], template_ids[4]], "barometro"))
        devices.append(([template_ids[2], template_ids[4]], "higrometro"))
        devices.append(([template_ids[3], template_ids[4]], "anemometro"))
        devices.append(([template_ids[0], template_ids[1],
                         template_ids[2], template_ids[3]], "instrumento de medicao"))
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
        devices.append(([template_ids[12]], "acesso"))
        devices.append(([template_ids[13]], "token"))
        devices.append(([template_ids[14]], "CameraQualcomm"))

        devices_ids = self.createDevices(jwt, devices)
        self.logger.info("devices ids: " + str(devices_ids))

        ###################
        # Configuring flows
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
                    "device_source_id": "anemometro (" + Api.get_deviceid_by_label(jwt, 'anemometro') + ")",
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
                [{"id": "3433da79.e543a6", "type": "tab", "label": "Flow 1"},
                 {"id": "5f77d972.391e98",
                    "type": "event template in",
                    "z": "3433da79.e543a6",
                    "name": "ônibus",
                    "event_create": False,
                    "event_update": False,
                    "event_remove": False,
                    "event_configure": False,
                    "event_publish": True,
                    "template_id": str(template_ids[5]),
                    "x": 154.5,
                    "y": 277,
                    "wires": [["845deaaf.f8cb98", "44c99e4.76b8a6"]]},
                 {"id": "845deaaf.f8cb98",
                    "type": "geofence",
                    "z": "3433da79.e543a6",
                    "name": "",
                    "mode": "polyline",
                    "filter": "inside",
                    "points":
                        [{"latitude": "-22.893729786643423",
                            "longitude": "-47.060708999633796"},
                         {"latitude": "-22.888827380892344",
                             "longitude": "-47.0570182800293"},
                         {"latitude": "-22.887720361534203",
                            "longitude": "-47.053241729736335"},
                         {"latitude": "-22.88724592190222",
                             "longitude": "-47.04869270324708"},
                         {"latitude": "-22.88692962789286",
                             "longitude": "-47.04483032226563"},
                         {"latitude": "-22.890646035948535",
                             "longitude": "-47.04671859741211"},
                         {"latitude": "-22.895073963731004",
                            "longitude": "-47.047061920166016"},
                         {"latitude": "-22.90013427567171",
                             "longitude": "-47.048091888427734"},
                         {"latitude": "-22.905589713001355",
                             "longitude": "-47.0463752746582"},
                         {"latitude": "-22.905115335858504",
                            "longitude": "-47.050237655639656"},
                         {"latitude": "-22.905115335858504",
                             "longitude": "-47.05195426940918"},
                         {"latitude": "-22.906143150903915",
                             "longitude": "-47.05530166625977"},
                         {"latitude": "-22.902427167370448",
                            "longitude": "-47.057275772094734"},
                         {"latitude": "-22.899027348564793",
                            "longitude": "-47.058563232421875"},
                         {"latitude": "-22.896813467251835", "longitude": "-47.05890655517578"}],
                    "geopoint": "payload.data.attrs.gps",
                    "x": 403.5,
                    "y": 158,
                    "wires": [["d905b5c9.4958e8"]]},
                 {"id": "d905b5c9.4958e8",
                    "type": "change",
                    "z": "3433da79.e543a6",
                    "name": "",
                    "rules":
                        [{"t": "set",
                            "p": "saida.mensagem",
                            "pt": "msg",
                            "to": "Está no Cambuí",
                            "tot": "str"}],
                    "action": "",
                    "property": "",
                    "from": "",
                    "to": "",
                    "reg": "false",
                    "x": 736.5,
                    "y": 153,
                    "wires": [["25c1c361.88827c"]]},
                 {"id": "44c99e4.76b8a6",
                    "type": "geofence",
                    "z": "3433da79.e543a6",
                    "name": "",
                    "mode": "polyline",
                    "filter": "outside",
                    "points":
                        [{"latitude": "-22.893729786643423",
                            "longitude": "-47.060708999633796"},
                         {"latitude": "-22.888827380892344",
                             "longitude": "-47.0570182800293"},
                         {"latitude": "-22.887720361534203",
                            "longitude": "-47.053241729736335"},
                         {"latitude": "-22.88724592190222",
                             "longitude": "-47.04869270324708"},
                         {"latitude": "-22.88692962789286",
                             "longitude": "-47.04483032226563"},
                         {"latitude": "-22.890646035948535",
                             "longitude": "-47.04671859741211"},
                         {"latitude": "-22.895073963731004",
                            "longitude": "-47.047061920166016"},
                         {"latitude": "-22.90013427567171",
                             "longitude": "-47.048091888427734"},
                         {"latitude": "-22.905589713001355",
                             "longitude": "-47.0463752746582"},
                         {"latitude": "-22.905115335858504",
                            "longitude": "-47.050237655639656"},
                         {"latitude": "-22.905115335858504",
                             "longitude": "-47.05195426940918"},
                         {"latitude": "-22.906143150903915",
                             "longitude": "-47.05530166625977"},
                         {"latitude": "-22.902427167370448",
                            "longitude": "-47.057275772094734"},
                         {"latitude": "-22.899027348564793",
                            "longitude": "-47.058563232421875"},
                         {"latitude": "-22.896813467251835", "longitude": "-47.05890655517578"}],
                    "geopoint": "payload.data.attrs.gps",
                    "x": 412,
                    "y": 372,
                    "wires": [["44d30981.231c48"]]},
                 {"id": "44d30981.231c48",
                    "type": "change",
                    "z": "3433da79.e543a6",
                    "name": "",
                    "rules":
                        [{"t": "set",
                            "p": "saida.mensagem",
                            "pt": "msg",
                            "to": "Não está no Cambuí",
                            "tot": "str"}],
                    "action": "",
                    "property": "",
                    "from": "",
                    "to": "",
                    "reg": "false",
                    "x": 773,
                    "y": 365,
                    "wires": [["25c1c361.88827c"]]},
                 {"id": "25c1c361.88827c",
                    "type": "multi device out",
                    "z": "3433da79.e543a6",
                    "name": "",
                    "device_source": "self",
                    "devices_source_dynamic": "",
                    "devices_source_dynamicFieldType": "msg",
                    "devices_source_configured": [""],
                    "_devices_loaded": "true",
                    "attrs": "saida",
                    "x": 1110.5,
                    "y": 225,
                    "wires": []}
                 ]
        })
        flows.append({
            "name": "http - POST",
            "flow": [
                {"id": "f66d93e3.8f42e", "type": "tab", "label": "Flow 1"},
                {"id": "853a54b9.f53208",
                 "type": "device template in",
                 "z": "f66d93e3.8f42e",
                 "name": "ônibus",
                 "device_template": {"id": template_ids[5]},
                 "status": "false",
                 "device_template_id": template_ids[5],
                 "x": 136.5,
                 "y": 144,
                 "wires": [["ce40a438.e567c8"]]},
                {"id": "784cd62a.09b088",
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
                 "wires": []},
                {"id": "ce40a438.e567c8",
                 "type": "switch",
                 "z": "f66d93e3.8f42e",
                 "name": "velocidade >= 50",
                 "property": "payload.velocidade",
                 "propertyType": "msg",
                 "rules": [{"t": "gte", "v": "50", "vt": "num"}],
                 "checkall": "true",
                 "outputs": "1",
                 "x": 409.5,
                 "y": 210,
                 "wires": [["5d51ecfa.baa4e4"]]},
                {"id": "5d51ecfa.baa4e4",
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
                 "wires": [["784cd62a.09b088"]]}
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
                      "device_source_id": "termometro Celsius(" + Api.get_deviceid_by_label(jwt, 'termometro Celsius') + ")",
                      "status": "false",
                      "_device_id": Api.get_deviceid_by_label(jwt, 'termometro Celsius'),
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

        # TODO: Adicionar o no remoto kelvin
        ##

        flows.append({
            "name": "kelvin flow",
            "flow":
                [{"id": "9d53e6e.1fcd818", "type": "tab", "label": "Flow 1"},
                 {"id": "bce46601.d18af8",
                  "type": "kelvin",
                  "z": "9d53e6e.1fcd818",
                  "name": "",
                  "out": "saida.temperatura",
                  "outFieldType": "msg",
                  "in": "payload.data.attrs.temperatura",
                  "inFieldType": "msg",
                  "x": 464.5,
                  "y": 186,
                  "wires": [["A633ec5fa67d97c"]]},
                 {"id": "Af6bcb284dcf69",
                  "type": "event device in",
                  "z": "9d53e6e.1fcd818",
                  "name": "termometro Celsius",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'termometro Celsius'),
                  "x": 204.5,
                  "y": 183,
                  "wires": [["bce46601.d18af8"]]},
                 {"id": "A633ec5fa67d97c",
                  "type": "multi device out",
                  "z": "9d53e6e.1fcd818",
                  "name": "termometro Kelvin",
                  "device_source": "configured",
                  "devices_source_dynamic": "",
                  "devices_source_dynamicFieldType": "msg",
                  "devices_source_configured": [Api.get_deviceid_by_label(jwt, 'termometro Kelvin')],
                  "attrs": "saida",
                  "_devices_loaded": True,
                  "x": 723.5,
                  "y": 181,
                  "wires": []}
                 ]
        })

        flows.append({
            "name": "device in flow",
            "flow":
                [{"id": "33fa4ae3.618106", "type": "tab", "label": "Flow 1"},
                 {"id": "48890b68.172a74",
                  "type": "device in",
                  "z": "33fa4ae3.618106",
                  "name": "device",
                  "device_source_id": "device (" + Api.get_deviceid_by_label(jwt, 'device') + ")",
                  "status": "false",
                  "_device_id": Api.get_deviceid_by_label(jwt, 'device'),
                  "_device_label": "",
                  "_device_type": "",
                  "x": 143.5,
                  "y": 182,
                  "wires": [["e776570c.cb9828"]]},
                 {"id": "e776570c.cb9828",
                  "type": "switch",
                  "z": "33fa4ae3.618106",
                  "name": "bool is true",
                  "property": "payload.bool",
                  "propertyType": "msg",
                  "rules": [{"t": "true"}],
                  "checkall": "true",
                  "outputs": "1",
                  "x": 315.5,
                  "y": 270,
                  "wires": [["1429c989.c2ede6"]]},
                 {"id": "1429c989.c2ede6",
                  "type": "change",
                  "z": "33fa4ae3.618106",
                  "name": "",
                  "rules":
                      [{"t": "set",
                        "p": "saida.str",
                        "pt": "msg",
                        "to": "teste do nó device in",
                        "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": "false",
                  "x": 501.5,
                  "y": 372,
                  "wires": [["93b073c2.ac4be"]]},
                 {"id": "f3326094.be251",
                  "type": "multi device out",
                  "z": "33fa4ae3.618106",
                  "name": "device",
                  "device_source": "dynamic",
                  "devices_source_dynamic": "deviceID",
                  "devices_source_dynamicFieldType": "msg",
                  "devices_source_configured": [Api.get_deviceid_by_label(jwt, 'device')],
                  "attrs": "saida",
                  "_devices_loaded": "true",
                  "x": 928.4999771118164,
                  "y": 543.0000381469727,
                  "wires": []},
                 {"id": "93b073c2.ac4be",
                  "type": "template",
                  "z": "33fa4ae3.618106",
                  "name": "",
                  "field": "deviceID",
                  "fieldType": "msg",
                  "syntax": "plain",
                  "template": Api.get_deviceid_by_label(jwt, 'device'),
                  "output": "str",
                  "x": 721.954833984375,
                  "y": 449.43753814697266,
                  "wires": [["f3326094.be251"]]}
                 ]
        })

        flows.append({
            "name": "switch e device out - deprecated nodes",
            "flow":
                [{"id": "1e495f9.c72c5a", "type": "tab", "label": "Flow 1"},
                 {"id": "79fcc2d9.4549cc",
                  "type": "device in",
                  "z": "1e495f9.c72c5a",
                  "name": "",
                  "device_source_id": "device (" + Api.get_deviceid_by_label(jwt, 'device') + "))",
                  "status": "false",
                  "_device_id": Api.get_deviceid_by_label(jwt, 'device'),
                  "_device_label": "",
                  "_device_type": "",
                  "x": 140.5,
                  "y": 152,
                  "wires": [["dc8f7863.74c0e8"]]},
                 {"id": "dc8f7863.74c0e8",
                  "type": "switch",
                  "z": "1e495f9.c72c5a",
                  "name": "int == 1",
                  "property": "payload.int",
                  "propertyType": "msg",
                  "rules": [{"t": "eq", "v": "1", "vt": "num"}],
                  "checkall": "true",
                  "outputs": 1,
                  "x": 276.5,
                  "y": 221,
                  "wires": [["405e4912.83c5c8"]]},
                 {"id": "405e4912.83c5c8",
                  "type": "change",
                  "z": "1e495f9.c72c5a",
                  "name": "",
                  "rules":
                      [{"t": "set",
                        "p": "saida.str",
                        "pt": "msg",
                        "to": "teste do nó switch",
                        "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 431.5,
                  "y": 313,
                  "wires": [["2455e7cf.24ceb8"]]},
                 {"id": "2455e7cf.24ceb8",
                  "type": "device out",
                  "z": "1e495f9.c72c5a",
                  "name": "",
                  "device_source": "self",
                  "device_source_msg": "",
                  "device_source_id": "",
                  "attrs": "saida",
                  "_device_id": "",
                  "x": 618.5,
                  "y": 446,
                  "wires": []}]
        })

        flows.append({
            "name": "actuate flow",
            "flow":
                [{"id": "7320e2d3.7984bc", "type": "tab", "label": "Flow 1"},
                 {"id": "a26f3b44.379118",
                  "type": "device template in",
                  "z": "7320e2d3.7984bc",
                  "name": "ônibus",
                  "device_template": {"id": template_ids[5]},
                  "status": "false",
                  "device_template_id": template_ids[5],
                  "x": 93.5,
                  "y": 226,
                  "wires": [["e98654fe.c42fa8"]]},
                 {"id": "e98654fe.c42fa8",
                  "type": "switch",
                  "z": "7320e2d3.7984bc",
                  "name": "passageiros >= 40",
                  "property": "payload.passageiros",
                  "propertyType": "msg",
                  "rules": [{"t": "gte", "v": "40", "vt": "num"}, {"t": "lt", "v": "40", "vt": "num"}],
                  "checkall": "true",
                  "outputs": 2,
                  "x": 305.5,
                  "y": 229,
                  "wires": [["7fd783d8.7fa12c"], ["f8be2e5c.7e6c7"]]},
                 {"id": "7fd783d8.7fa12c",
                  "type": "change",
                  "z": "7320e2d3.7984bc",
                  "name": "LOTADO",
                  "rules":
                      [{"t": "set",
                        "p": "saida.letreiro",
                        "pt": "msg",
                        "to": "LOTADO",
                        "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 551.5,
                  "y": 142,
                  "wires": [["af8485c5.8352d8"]]},
                 {"id": "af8485c5.8352d8",
                  "type": "multi actuate",
                  "z": "7320e2d3.7984bc",
                  "name": "",
                  "device_source": "self",
                  "devices_source_configured": [""],
                  "devices_source_dynamic": "",
                  "devices_source_dynamicFieldType": "msg",
                  "attrs": "saida",
                  "_devices_loaded": True,
                  "x": 816.5,
                  "y": 228,
                  "wires": []},
                 {"id": "f8be2e5c.7e6c7",
                  "type": "change",
                  "z": "7320e2d3.7984bc",
                  "name": "JARDIM PAULISTA",
                  "rules":
                      [{"t": "set",
                        "p": "saida.letreiro",
                        "pt": "msg",
                        "to": "JARDIM PAULISTA",
                        "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 576,
                  "y": 313,
                  "wires": [["af8485c5.8352d8"]]}]
        })

        flows.append({
            "name": "notification flow",
            "flow":
                [{"id": "ea21ed04.e04c9", "type": "tab", "label": "Flow 1"},
                 {"id": "6971025a.64948c",
                  "type": "event template in",
                  "z": "ea21ed04.e04c9",
                  "name": "TesteTemplate",
                  "event_create": False,
                  "event_update": False,
                  "event_remove": False,
                  "event_configure": False,
                  "event_publish": True,
                  "template_id": str(template_ids[7]),
                  "x": 83.94790649414062,
                  "y": 107.18403625488281,
                  "wires": [["91cde1ab.a5e9e"]]},
                 {"id": "91cde1ab.a5e9e",
                  "type": "switch",
                  "z": "ea21ed04.e04c9",
                  "name": "int >= 0",
                  "property": "payload.data.attrs.int",
                  "propertyType": "msg",
                  "rules": [{"t": "gte", "v": "0", "vt": "num"}],
                  "checkall": "true",
                  "outputs": 1,
                  "x": 282.94798278808594,
                  "y": 207.43401908874512,
                  "wires": [["4395ba8.454c144"]]},
                 {"id": "d708a3a6.a6735",
                  "type": "notification",
                  "z": "ea21ed04.e04c9",
                  "name": "notificação",
                  "source": "notification.metadata",
                  "sourceFieldType": "msg",
                  "messageDynamic": "notification.message",
                  "messageStatic": "",
                  "messageFieldType": "msg",
                  "msgType": "dynamic",
                  "x": 700.9514617919922,
                  "y": 545.302188873291,
                  "wires": [[]]},
                 {"id": "4395ba8.454c144",
                  "type": "template",
                  "z": "ea21ed04.e04c9",
                  "name": "",
                  "field": "notification",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{\"message\":\"teste do nó notification\",\n\"metadata\":{\"prioridade\":\"baixa\"}\n}",
                  "output": "json",
                  "x": 382.9549255371094,
                  "y": 316.4236068725586,
                  "wires": [["d708a3a6.a6735"]]}]
        })

        flows.append({
            "name": "FTP",
            "enabled": True,
            "id": "2a6511dc-8ad1-4a58-ab42-213281d63d3f",
            "flow":
                [
                    {"id": "81f229c7.c43d88", "type": "tab", "label": "Fluxo 1"},
                    {"id": "a2ddb012.598d1",
                     "type": "ftp",
                     "z": "81f229c7.c43d88",
                     "name": "",
                     "method": "PUT",
                     "url": "ftp://10.202.71.7",
                     "username": "dojot",
                     "password": "dojot",
                     "filename": "data_filename",
                     "filecontent": "data_content",
                     "fileencoding": "utf-8",
                     "response": "ftp_output",
                     "x": 817.5,
                     "y": 301,
                     "wires": [[]]},
                    {"id": "1644ae1e.ca0d72",
                     "type": "template",
                     "z": "81f229c7.c43d88",
                     "name": "data filename",
                     "field": "data_filename",
                     "fieldType": "msg",
                     "syntax": "handlebars",
                     "template": "{{payload.data.attrs.band}}-{{payloadMetadata.timestamp}}.txt",
                     "output": "str",
                     "x": 615.5,
                     "y": 194.5,
                     "wires": [["ced523a0.dc0168", "c988bf58.bcfff8"]]},
                    {"id": "dfbec05a.9604c8",
                     "type": "template",
                     "z": "81f229c7.c43d88",
                     "name": "image filename",
                     "field": "image_filename",
                     "fieldType": "msg",
                     "syntax": "handlebars",
                     "template": "{{payload.data.attrs.band}}-{{payloadMetadata.timestamp}}-01.jpg",
                     "output": "str",
                     "x": 199,
                     "y": 194,
                     "wires": [["7526eed9.4b4c98"]]},
                    {"id": "7526eed9.4b4c98",
                     "type": "template",
                     "z": "81f229c7.c43d88",
                     "name": "data content",
                     "field": "data_content",
                     "fieldType": "msg",
                     "syntax": "handlebars",
                     "template": "datahora: {{payloadMetadata.timestamp}}\nfaixa: {{payload.data.attrs.band}}\nplaca: {{payload.data.attrs.license_plate}}\ncoordenadas: {{payload.data.attrs.coordinates}}\nclassificacao: {{payload.data.attrs.vehicle_type}}\nimagens: {{image_filename}}",
                     "output": "str",
                     "x": 406.5,
                     "y": 193.5,
                     "wires": [["1644ae1e.ca0d72"]]},
                    {"id": "ced523a0.dc0168",
                     "type": "ftp",
                     "z": "81f229c7.c43d88",
                     "name": "",
                     "method": "PUT",
                     "url": "ftp://10.202.71.7",
                     "username": "dojot",
                     "password": "dojot",
                     "filename": "image_filename",
                     "filecontent": "payload.data.attrs.image",
                     "fileencoding": "base64",
                     "response": "ftp_output",
                     "x": 595,
                     "y": 300,
                     "wires": [["a2ddb012.598d1"]]},
                    {"id": "c988bf58.bcfff8",
                     "type": "ftp",
                     "z": "81f229c7.c43d88",
                     "name": "",
                     "method": "PUT",
                     "url": "ftp://192.168.0.38",
                     "username": "dojot",
                     "password": "dojot",
                     "filename": "image_filename",
                     "filecontent": "payload.data.attrs.image",
                     "fileencoding": "base64",
                     "response": "ftp_output",
                     "x": 597,
                     "y": 375,
                     "wires": [["167a2f5a.3e56d9"]]},
                    {"id": "167a2f5a.3e56d9",
                     "type": "ftp",
                     "z": "81f229c7.c43d88",
                     "name": "",
                     "method": "PUT",
                     "url": "ftp://192.168.0.38",
                     "username": "dojot",
                     "password": "dojot",
                     "filename": "data_filename",
                     "filecontent": "data_content",
                     "fileencoding": "utf-8",
                     "response": "ftp_output",
                     "x": 819.5,
                     "y": 376,
                     "wires": [[]]},
                    {"id": "Abfe0a08f78ae6",
                     "type": "event template in",
                     "z": "81f229c7.c43d88",
                     "name": "",
                     "event_create": False,
                     "event_update": False,
                     "event_remove": False,
                     "event_configure": False,
                     "event_publish": True,
                     "template_id": str(template_ids[8]),
                     "x": 125.5,
                     "y": 96,
                     "wires": [["dfbec05a.9604c8"]]}]
        })

        device_id = Api.get_deviceid_by_label(jwt, 'device')
        dispositivo_id = Api.get_deviceid_by_label(jwt, "dispositivo")
        current_time = int(time.time() * 1000)

        flows.append({
            "name": "CRON-BATCH-BROKER",
            "enabled": True,
            "id": "22083bd7-f38d-4f8a-9bf5-ee03f99440b1",
            "flow":
                [{"id": "A23f9977470ec28", "type": "tab", "label": "Flow 1"},
                 {"id": "A2f3cb557972b8a",
                  "type": "event device in",
                  "z": "A23f9977470ec28",
                  "name": "dispositivo",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'dispositivo'),
                  "x": 88.5,
                  "y": 131,
                  "wires": [["A29ed3c72e57774"]]},
                 {"id": "A141239ec4d6ef6",
                  "type": "cron-batch",
                  "z": "A23f9977470ec28",
                  "name": "remove job",
                  "operation": "REMOVE",
                  "jobs": "",
                  "jobsType": "msg",
                  "inJobIds": "mergedData.job_id",
                  "inJobIdsType": "msg",
                  "outJobIds": "",
                  "outJobIdsType": "msg",
                  "timeout": "1000",
                  "x": 1120.5,
                  "y": 359,
                  "wires": [[]]},
                 {"id": "A29ed3c72e57774",
                  "type": "switch",
                  "z": "A23f9977470ec28",
                  "name": "is true",
                  "property": "payload.data.attrs.bool",
                  "propertyType": "msg",
                  "rules": [{"t": "true"}, {"t": "else"}],
                  "checkall": "true",
                  "outputs": 2,
                  "x": 274.5,
                  "y": 130,
                  "wires": [["Aeffb33b3eaebd"], ["Aaec0ef5ae39d6"]]},
                 {"id": "Ae606f5d2fbbfd8",
                  "type": "cron-batch",
                  "z": "A23f9977470ec28",
                  "name": "create job",
                  "operation": "CREATE",
                  "jobs": "reqJOB",
                  "jobsType": "msg",
                  "inJobIds": "",
                  "inJobIdsType": "msg",
                  "outJobIds": "out.job_id",
                  "outJobIdsType": "msg",
                  "timeout": "1000",
                  "x": 755.5,
                  "y": 60,
                  "wires": [["A16c85e9bdd2e01"]]},
                 {"id": "Aeffb33b3eaebd",
                  "type": "template",
                  "z": "A23f9977470ec28",
                  "name": "",
                  "field": "reqJOB",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "[          \n  {\n    \"time\": \"*/3 * * * *\",\n    \"timezone\": \"America/Sao_Paulo\",\n    \"name\": \"Keep alive\",\n    \"description\": \"This job sends a keep alive notification to a device every 3 minutes\",\n    \"broker\": {\n        \"subject\": \"dojot.device-manager.device\",\n        \"message\": {\n               \"event\":\"configure\",\n                \"meta\": {\n                    \"service\": \"admin\",\n                    \"timestamp\": "+str(current_time)+"},\n               \"data\": {\n                   \"attrs\": { \"mensagem\": \"keepalive\"},\n                   \"id\": \""+dispositivo_id+"\" \n                }\n        }\n    }\n   }\n]",
                  "output": "json",
                  "x": 494.5,
                  "y": 61,
                  "wires": [["Ae606f5d2fbbfd8"]]},
                 {"id": "A16c85e9bdd2e01",
                  "type": "merge data",
                  "z": "A23f9977470ec28",
                  "name": "",
                  "targetData": "out",
                  "mergedData": "mergedData",
                  "x": 848.5,
                  "y": 193,
                  "wires": [["A519d0e748f6f2"]]},
                 {"id": "A519d0e748f6f2",
                  "type": "switch",
                  "z": "A23f9977470ec28",
                  "name": "is false",
                  "property": "payload.data.attrs.bool",
                  "propertyType": "msg",
                  "rules": [{"t": "false"}],
                  "checkall": "true",
                  "outputs": 1,
                  "x": 1012,
                  "y": 275,
                  "wires": [["A141239ec4d6ef6"]]},
                 {"id": "Aaec0ef5ae39d6",
                  "type": "change",
                  "z": "A23f9977470ec28",
                  "name": "",
                  "rules":
                      [{"t": "set", "p": "out.dummy", "pt": "msg",
                          "to": "true", "tot": "bool"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 522.5,
                  "y": 198,
                  "wires": [["A16c85e9bdd2e01"]]}]
        })

        flows.append({
            "name": "CRON-BATCH-HTTP",
            "enabled": True,
            "id": "22083bd7-f38d-4f8a-9bf5-ee03f99440b1",
            "flow":
                [{"id": "A23f9977470ec28", "type": "tab", "label": "Flow 1"},
                 {"id": "A2f3cb557972b8a",
                  "type": "event device in",
                  "z": "A23f9977470ec28",
                  "name": "device",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'device'),
                  "x": 88.5,
                  "y": 131,
                  "wires": [["A29ed3c72e57774"]]},
                 {"id": "A29ed3c72e57774",
                  "type": "switch",
                  "z": "A23f9977470ec28",
                  "name": "is true",
                  "property": "payload.data.attrs.bool",
                  "propertyType": "msg",
                  "rules": [{"t": "true"}, {"t": "else"}],
                  "checkall": "true",
                  "outputs": 2,
                  "x": 274.5,
                  "y": 130,
                  "wires": [["Aeffb33b3eaebd"], ["Ad0eb70ff85569"]]},
                 {"id": "Ae606f5d2fbbfd8",
                  "type": "cron-batch",
                  "z": "A23f9977470ec28",
                  "name": "create job",
                  "operation": "CREATE",
                  "jobs": "reqJOB",
                  "jobsType": "msg",
                  "inJobIds": "",
                  "inJobIdsType": "msg",
                  "outJobIds": "out.job_id",
                  "outJobIdsType": "msg",
                  "timeout": "1000",
                  "x": 755.5,
                  "y": 60,
                  "wires": [["A8305ee4570acd"]]},
                 {"id": "Aeffb33b3eaebd",
                  "type": "template",
                  "z": "A23f9977470ec28",
                  "name": "",
                  "field": "reqJOB",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "[    \n{\n   \"time\":\"*/2 * * * *\",\n   \"timezone\": \"America/Sao_Paulo\",\n   \"name\": \"Keep alive\",\n   \"description\": \"This job sends a keep alive notification to a device every 2 minutes\",\n   \"http\": {\n  \"method\": \"PUT\",\n   \"headers\": {\n   \"Authorization\": \"Bearer "+jwt+"\",\n   \"Content-Type\": \"application/json\"\n       },\n   \"url\": \"http://device-manager:5000/device/"+device_id+"/actuate\",\n   \"body\": {\n    \"attrs\": {\n   \"mensagem\": \"tô vivo\"\n  }\n    }\n    }\n   }]",
                  "output": "json",
                  "x": 535.5,
                  "y": 71,
                  "wires": [["Ae606f5d2fbbfd8"]]},
                 {"id": "Ad0eb70ff85569",
                  "type": "change",
                  "z": "A23f9977470ec28",
                  "name": "",
                  "rules":
                      [{"t": "set", "p": "out.dummy", "pt": "msg",
                          "to": "true", "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 553.5,
                  "y": 210,
                  "wires": [["A8305ee4570acd"]]},
                 {"id": "A8305ee4570acd",
                  "type": "merge data",
                  "z": "A23f9977470ec28",
                  "name": "",
                  "targetData": "out",
                  "mergedData": "mergedData",
                  "x": 901.5,
                  "y": 196,
                  "wires": [["A8f928cb058a08"]]},
                 {"id": "A8f928cb058a08",
                  "type": "switch",
                  "z": "A23f9977470ec28",
                  "name": "is false",
                  "property": "payload.data.attrs.bool",
                  "propertyType": "msg",
                  "rules": [{"t": "false"}],
                  "checkall": "true",
                  "outputs": 1,
                  "x": 1076.5,
                  "y": 285,
                  "wires": [["Aae84ce74de475"]]},
                 {"id": "Aae84ce74de475",
                  "type": "cron-batch",
                  "z": "A23f9977470ec28",
                  "name": "remove job",
                  "operation": "REMOVE",
                  "jobs": "reqJOB",
                  "jobsType": "msg",
                  "inJobIds": "mergedData.job_id",
                  "inJobIdsType": "msg",
                  "outJobIds": "out.job_id",
                  "outJobIdsType": "msg",
                  "timeout": "1000",
                  "x": 1262,
                  "y": 350,
                  "wires": [[]]}]
        })

        time.sleep(1)
        current_time = int(time.time() * 1000)

        flows.append({
            "name": "CRON-EventRequest",
            "enabled": True,
            "id": "22083bd7-f38d-4f8a-9bf5-ee03f99440b1",
            "flow":
                [{"id": "A6a8342f975d99c", "type": "tab", "label": "Flow 1"},
                 {"id": "Aa7942dad3588b",
                  "type": "event device in",
                  "z": "A6a8342f975d99c",
                  "name": "dispositivo",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'dispositivo'),
                  "x": 94.5,
                  "y": 82,
                  "wires": [["A2fbb952985265a"]]},
                 {"id": "A2fbb952985265a",
                  "type": "switch",
                  "z": "A6a8342f975d99c",
                  "name": "",
                  "property": "payload.data.attrs.bool",
                  "propertyType": "msg",
                  "rules": [{"t": "true"}, {"t": "else"}],
                  "checkall": "true",
                  "outputs": 2,
                  "x": 290.5,
                  "y": 189,
                  "wires": [["A67adb70f0693a8"], ["Acdcd6b5508fae8"]]},
                 {"id": "A67adb70f0693a8",
                  "type": "template",
                  "z": "A6a8342f975d99c",
                  "name": "",
                  "field": "jobAction",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{\n    \"subject\": \"dojot.device-manager.device\",\n    \"message\": {\n            \"event\":\"configure\",\n            \"meta\": {\n              \"service\":\"admin\",\n              \"timestamp\": "+str(current_time)+"              \n            },\n            \"data\": {\n                \"attrs\": { \"mensagem\": \"keepalive2\"},\n                \"id\": \""+dispositivo_id+"\"\n            }\n    }\n}",
                  "output": "json",
                  "x": 539.5,
                  "y": 171,
                  "wires": [["Af966cf116860c"]]},
                 {"id": "Af966cf116860c",
                  "type": "cron",
                  "z": "A6a8342f975d99c",
                  "name": "create job",
                  "operation": "CREATE",
                  "cronTimeExpression": "*/2 * * * *",
                  "jobName": "keepalive2",
                  "jobDescription": "Esse job envia notificação de keepalive2 a cada 2 minutos",
                  "jobType": "EVENT REQUEST",
                  "jobAction": "jobAction",
                  "jobActionType": "msg",
                  "inJobId": "jobID",
                  "inJobIdType": "msg",
                  "outJobId": "out.jobID",
                  "outJobIdType": "msg",
                  "x": 754.5,
                  "y": 171,
                  "wires": [["A2fc9e73a35dc58"]]},
                 {"id": "Acdcd6b5508fae8",
                  "type": "change",
                  "z": "A6a8342f975d99c",
                  "name": "",
                  "rules":
                      [{"t": "set", "p": "out.dummy", "pt": "msg",
                          "to": "dummy", "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 484.5,
                  "y": 314,
                  "wires": [["A2fc9e73a35dc58"]]},
                 {"id": "A2fc9e73a35dc58",
                  "type": "merge data",
                  "z": "A6a8342f975d99c",
                  "name": "",
                  "targetData": "out",
                  "mergedData": "merged",
                  "x": 880.5,
                  "y": 302,
                  "wires": [["A42c70517200b6c"]]},
                 {"id": "A42c70517200b6c",
                  "type": "switch",
                  "z": "A6a8342f975d99c",
                  "name": "",
                  "property": "payload.data.attrs.bool",
                  "propertyType": "msg",
                  "rules": [{"t": "false"}],
                  "checkall": "true",
                  "outputs": 1,
                  "x": 1042.5,
                  "y": 386,
                  "wires": [["A5e75a6acbb46f8"]]},
                 {"id": "A5e75a6acbb46f8",
                  "type": "cron",
                  "z": "A6a8342f975d99c",
                  "name": "",
                  "operation": "REMOVE",
                  "cronTimeExpression": "",
                  "jobName": "",
                  "jobDescription": "",
                  "jobType": "EVENT REQUEST",
                  "jobAction": "",
                  "jobActionType": "msg",
                  "inJobId": "merged.jobID",
                  "inJobIdType": "msg",
                  "outJobId": "",
                  "outJobIdType": "msg",
                  "x": 1208.5,
                  "y": 450,
                  "wires": [[]]}]
        })

        flows.append({
            "name": "CRON-HTTPRequest",
            "enabled": True,
            "id": "22083bd7-f38d-4f8a-9bf5-ee03f99440b1",
            "flow":
                [{"id": "A2720aa5be2e886", "type": "tab", "label": "Flow 1"},
                 {"id": "Adc2f7c69fe575",
                  "type": "cron",
                  "z": "A2720aa5be2e886",
                  "name": "",
                  "operation": "CREATE",
                  "cronTimeExpression": "*/3 * * * *",
                  "jobName": "tô vivo 2",
                  "jobDescription": "Esse job envia notificação de tô vivo 2 a cada 3 minutos",
                  "jobType": "HTTP REQUEST",
                  "jobAction": "jobAction",
                  "jobActionType": "msg",
                  "inJobId": "jobID",
                  "inJobIdType": "msg",
                  "outJobId": "out.jobID",
                  "outJobIdType": "msg",
                  "x": 684.5,
                  "y": 170,
                  "wires": [["A3d7c25c1d4920a"]]},
                 {"id": "A48e2fd463c7d04",
                  "type": "event device in",
                  "z": "A2720aa5be2e886",
                  "name": "device",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'device'),
                  "x": 134.5,
                  "y": 76,
                  "wires": [["A2efbb79f0a80c8"]]},
                 {"id": "A2efbb79f0a80c8",
                  "type": "switch",
                  "z": "A2720aa5be2e886",
                  "name": "",
                  "property": "payload.data.attrs.bool",
                  "propertyType": "msg",
                  "rules": [{"t": "true"}, {"t": "else"}],
                  "checkall": "true",
                  "outputs": 2,
                  "x": 298.5,
                  "y": 170,
                  "wires": [["A64677826f45048"], ["Acc6448ca9d8a88"]]},
                 {"id": "A64677826f45048",
                  "type": "template",
                  "z": "A2720aa5be2e886",
                  "name": "",
                  "field": "jobAction",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{\n\n \"method\": \"PUT\",\n \"headers\": {\n      \"Authorization\": \"Bearer "+jwt+"\",\n      \"Content-Type\": \"application/json\"\n      },\n      \"url\": \"http://device-manager:5000/device/"+device_id+"/actuate\",\n      \"body\": {\n                \"attrs\": {\"mensagem\": \"tô vivo 2\"}\n               }\n}",
                  "output": "json",
                  "x": 518,
                  "y": 95,
                  "wires": [["Adc2f7c69fe575"]]},
                 {"id": "Acc6448ca9d8a88",
                  "type": "change",
                  "z": "A2720aa5be2e886",
                  "name": "",
                  "rules":
                      [{"t": "set", "p": "out.dummy", "pt": "msg",
                          "to": "dummy", "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 531.5,
                  "y": 259,
                  "wires": [["A3d7c25c1d4920a"]]},
                 {"id": "A3d7c25c1d4920a",
                  "type": "merge data",
                  "z": "A2720aa5be2e886",
                  "name": "",
                  "targetData": "out",
                  "mergedData": "merged",
                  "x": 798.5,
                  "y": 295,
                  "wires": [["A51a4fbd84b9664"]]},
                 {"id": "A51a4fbd84b9664",
                  "type": "switch",
                  "z": "A2720aa5be2e886",
                  "name": "",
                  "property": "payload.data.attrs.bool",
                  "propertyType": "msg",
                  "rules": [{"t": "false"}],
                  "checkall": "true",
                  "outputs": 1,
                  "x": 996.5,
                  "y": 390,
                  "wires": [["A82d5cd61eb817"]]},
                 {"id": "A82d5cd61eb817",
                  "type": "cron",
                  "z": "A2720aa5be2e886",
                  "name": "",
                  "operation": "REMOVE",
                  "cronTimeExpression": "",
                  "jobName": "",
                  "jobDescription": "",
                  "jobType": "EVENT REQUEST",
                  "jobAction": "",
                  "jobActionType": "msg",
                  "inJobId": "merged.jobID",
                  "inJobIdType": "msg",
                  "outJobId": "",
                  "outJobIdType": "msg",
                  "x": 1098.5,
                  "y": 474,
                  "wires": [[]]}]
        })

        flows.append({
            "name": "http-notification flow",
            "flow":
                [{"id": "A59438adde7b684", "type": "tab", "label": "Flow 1"},
                 {"id": "Ad1babd3c07d14",
                  "type": "event device in",
                  "z": "A59438adde7b684",
                  "name": "device",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'device'),
                  "x": 288.5,
                  "y": 78,
                  "wires": [["A54935028169bb"]]},
                 {"id": "Ae593bc2cb200a",
                  "type": "http",
                  "z": "A59438adde7b684",
                  "name": "",
                  "method": "POST",
                  "ret": "txt",
                  "body": "reqBody",
                  "response": "responseGET",
                  "url": "http://ptsv2.com/t/3fbhu-1543424220/post",
                  "x": 700.5,
                  "y": 350,
                  "wires": [["A1b4ddf2b1bdf91"]]},
                 {"id": "A1b4ddf2b1bdf91",
                  "type": "notification",
                  "z": "A59438adde7b684",
                  "name": "",
                  "source": "responseGET",
                  "sourceFieldType": "msg",
                  "messageDynamic": "",
                  "messageStatic": "mensagem estática",
                  "messageFieldType": "msg",
                  "msgType": "static",
                  "x": 887.5,
                  "y": 438,
                  "wires": []},
                 {"id": "A54935028169bb",
                  "type": "switch",
                  "z": "A59438adde7b684",
                  "name": "",
                  "property": "payload.data.attrs.bool",
                  "propertyType": "msg",
                  "rules": [{"t": "true"}],
                  "checkall": "true",
                  "outputs": 1,
                  "x": 422.5,
                  "y": 161,
                  "wires": [["A2f1d3867539fa8"]]},
                 {"id": "A2f1d3867539fa8",
                  "type": "template",
                  "z": "A59438adde7b684",
                  "name": "",
                  "field": "reqBody",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{\"payload\": \"valor do atributo: {{payload.data.attrs.bool}}\"}",
                  "output": "str",
                  "x": 539.5,
                  "y": 256,
                  "wires": [["Ae593bc2cb200a"]]}
                 ]
        })

        flows.append({
            "name": "http - GET",
            "flow":
                [{"id": "A59438adde7b684", "type": "tab", "label": "Flow 1"},
                 {"id": "Ad1babd3c07d14",
                  "type": "event device in",
                  "z": "A59438adde7b684",
                  "name": "device",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'Pluviometro'),
                  "x": 289.5,
                  "y": 96,
                  "wires": [["A2f1d3867539fa8"]]},
                 {"id": "Ae593bc2cb200a",
                  "type": "http",
                  "z": "A59438adde7b684",
                  "name": "",
                  "method": "GET",
                  "ret": "txt",
                  "body": "reqBody",
                  "response": "responseGET",
                  "url": "http://ptsv2.com/t/3fbhu-1543424220/post",
                  "x": 631.5,
                  "y": 347,
                  "wires": [["A1b4ddf2b1bdf91"]]},
                 {"id": "A1b4ddf2b1bdf91",
                  "type": "notification",
                  "z": "A59438adde7b684",
                  "name": "",
                  "source": "responseGET",
                  "sourceFieldType": "msg",
                  "messageDynamic": "",
                  "messageStatic": "teste",
                  "messageFieldType": "msg",
                  "msgType": "static",
                  "x": 828.5,
                  "y": 436,
                  "wires": []},
                 {"id": "A2f1d3867539fa8",
                  "type": "template",
                  "z": "A59438adde7b684",
                  "name": "",
                  "field": "reqBody",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{\"payload\": \"valor do atributo: {{payload.data.attrs.chuva}}\"}",
                  "output": "str",
                  "x": 456.5,
                  "y": 186,
                  "wires": [["Ae593bc2cb200a"]]}
                 ]
        })

        flows.append({
            "name": "cumulative_sum flow",
            "flow":
                [{"id": "Aa5786bec575688", "type": "tab", "label": "Flow 1"},
                 {"id": "Aae8b509d09fde",
                  "type": "event device in",
                  "z": "Aa5786bec575688",
                  "name": "Pluviômetro",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'Pluviometro'),
                  "x": 129.5,
                  "y": 94,
                  "wires": [["A3a451b74879f44"]]},
                 {"id": "A99549f34d5f4d",
                  "type": "multi device out",
                  "z": "Aa5786bec575688",
                  "name": "controle",
                  "device_source": "configured",
                  "devices_source_dynamic": "",
                  "devices_source_dynamicFieldType": "msg",
                  "devices_source_configured": [Api.get_deviceid_by_label(jwt, "controle")],
                  "attrs": "saida",
                  "_devices_loaded": True,
                  "x": 648.5,
                  "y": 324,
                  "wires": []},
                 {"id": "A3a451b74879f44",
                  "type": "cumulative sum",
                  "z": "Aa5786bec575688",
                  "name": "chuva acumulada",
                  "timePeriod": "60",
                  "targetAttribute": "payload.data.attrs.chuva",
                  "timestamp": "payload.metadata.timestamp",
                  "output": "payload.data.attrs.chuva60min",
                  "fieldType": "msg",
                  "x": 293.5,
                  "y": 179,
                  "wires": [["Aae4a6506210738"]]},
                 {"id": "Aae4a6506210738",
                  "type": "template",
                  "z": "Aa5786bec575688",
                  "name": "",
                  "field": "saida.medida",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{{payload.data.attrs.chuva60min}}",
                  "output": "str",
                  "x": 479.5,
                  "y": 255,
                  "wires": [["A99549f34d5f4d"]]}
                 ]
        })

        flows.append({
            "name": "merge_data flow",
            "flow":
                [{"id": "A762d3498b7839c", "type": "tab", "label": "Flow 1"},
                 {"id": "Ac7b1472ac3dd58",
                  "type": "event device in",
                  "z": "A762d3498b7839c",
                  "name": "anemômetro",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'anemometro'),
                  "x": 164.5,
                  "y": 101,
                  "wires": [["A57c8a7faf15648"]]},
                 {"id": "Af03db7b122c7a8",
                  "type": "event device in",
                  "z": "A762d3498b7839c",
                  "name": "barômetro",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'barometro'),
                  "x": 166.5,
                  "y": 234,
                  "wires": [["A57c8a7faf15648"]]},
                 {"id": "A286bf51152805a",
                  "type": "multi device out",
                  "z": "A762d3498b7839c",
                  "name": "logger",
                  "device_source": "configured",
                  "devices_source_dynamic": "",
                  "devices_source_dynamicFieldType": "msg",
                  "devices_source_configured": [Api.get_deviceid_by_label(jwt, 'logger')],
                  "attrs": "merged",
                  "_devices_loaded": True,
                  "x": 643.5,
                  "y": 162,
                  "wires": []},
                 {"id": "A57c8a7faf15648",
                  "type": "merge data",
                  "z": "A762d3498b7839c",
                  "name": "",
                  "targetData": "payload.data.attrs",
                  "mergedData": "merged.data.attrs",
                  "x": 376.5,
                  "y": 161,
                  "wires": [["A286bf51152805a"]]}
                 ]
        })

        flows.append({
            "name": "cumulative_sum e merge_data flow",
            "flow":
                [{"id": "A55797f9442adc", "type": "tab", "label": "Flow 1"},
                 {"id": "A2a256d10f86a94",
                  "type": "event device in",
                  "z": "A55797f9442adc",
                  "name": "Pluviometro",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'Pluviometro'),
                  "x": 95.5,
                  "y": 95,
                  "wires": [["A184434ef231dcb"]]},
                 {"id": "A58c0cfd3eccc",
                  "type": "event device in",
                  "z": "A55797f9442adc",
                  "name": "Nível da água",
                  "event_configure": False,
                  "event_publish": True,
                  "device_id": Api.get_deviceid_by_label(jwt, 'SensorNivel'),
                  "x": 104.5,
                  "y": 309,
                  "wires": [["A52e9318932cdb"]]},
                 {"id": "A184434ef231dcb",
                  "type": "cumulative sum",
                  "z": "A55797f9442adc",
                  "name": "chuva na última hora",
                  "timePeriod": "60",
                  "targetAttribute": "payload.data.attrs.chuva",
                  "timestamp": "payload.metadata.timestamp",
                  "output": "payload.data.attrs.chuva60min",
                  "fieldType": "msg",
                  "x": 331.5,
                  "y": 175,
                  "wires": [["A52e9318932cdb"]]},
                 {"id": "A52e9318932cdb",
                  "type": "merge data",
                  "z": "A55797f9442adc",
                  "name": "",
                  "targetData": "payload.data.attrs",
                  "mergedData": "merged.data.attrs",
                  "x": 573.5,
                  "y": 306,
                  "wires": [["A74c426b82930d8", "A680a122a44734c"]]},
                 {"id": "A44394d8158b194",
                  "type": "switch",
                  "z": "A55797f9442adc",
                  "name": "nível > 2.5m",
                  "property": "merged.data.attrs.nivel",
                  "propertyType": "msg",
                  "rules":
                      [{"t": "btwn", "v": "2", "vt": "num", "v2": "2.5", "v2t": "num"},
                       {"t": "gt", "v": "2.5", "vt": "num"}],
                  "checkall": "false",
                  "outputs": 2,
                  "x": 816.5,
                  "y": 531,
                  "wires": [["A93ed17542a9d58"], ["Af52d095f6f9e48"]]},
                 {"id": "A93ed17542a9d58",
                  "type": "template",
                  "z": "A55797f9442adc",
                  "name": "Risco elevado de enchente",
                  "field": "notification",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{\"message\":\"Alertar Defesa Civil\",\n \"metadata\":{\"motivo\":\"Risco Elevado de Enchente\"}\n}",
                  "output": "json",
                  "x": 1089,
                  "y": 616,
                  "wires": [["Ae74fe8fec3a9e8"]]},
                 {"id": "Af52d095f6f9e48",
                  "type": "template",
                  "z": "A55797f9442adc",
                  "name": "Estado de enchente",
                  "field": "notification",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{\"message\":\"Acionar Alarme\",\n \"metadata\":{\"motivo\":\"Estado de Enchente\"}\n}",
                  "output": "json",
                  "x": 1073,
                  "y": 437,
                  "wires": [["Ae74fe8fec3a9e8"]]},
                 {"id": "A74c426b82930d8",
                  "type": "switch",
                  "z": "A55797f9442adc",
                  "name": "chuva (na última hora) > 20mm",
                  "property": "merged.data.attrs.chuva60min",
                  "propertyType": "msg",
                  "rules": [{"t": "gt", "v": "20", "vt": "num"}],
                  "checkall": "true",
                  "outputs": 1,
                  "x": 683.5,
                  "y": 413,
                  "wires": [["A44394d8158b194"]]},
                 {"id": "Ae74fe8fec3a9e8",
                  "type": "notification",
                  "z": "A55797f9442adc",
                  "name": "",
                  "source": "notification.metadata",
                  "sourceFieldType": "msg",
                  "messageDynamic": "notification.message",
                  "messageStatic": "",
                  "messageFieldType": "msg",
                  "msgType": "dynamic",
                  "x": 1351.5,
                  "y": 513,
                  "wires": []},
                 {"id": "A680a122a44734c",
                  "type": "multi device out",
                  "z": "A55797f9442adc",
                  "name": "logger",
                  "device_source": "configured",
                  "devices_source_dynamic": "",
                  "devices_source_dynamicFieldType": "msg",
                  "devices_source_configured": [Api.get_deviceid_by_label(jwt, 'logger')],
                  "attrs": "merged",
                  "_devices_loaded": True,
                  "x": 813.5,
                  "y": 241,
                  "wires": []}
                 ]
        })

        flows.append({
            "name": "actuate Raspberry Pi",
            "flow":
                [{"id": "A37b7b487ab5cac", "type": "tab", "label": "Flow 1"},
                 {"id": "A3615bef97f5552",
                  "type": "event template in",
                  "z": "A37b7b487ab5cac",
                  "name": "Raspberry Pi",
                  "event_create": False,
                  "event_update": False,
                  "event_remove": False,
                  "event_configure": False,
                  "event_publish": True,
                  "template_id": str(template_ids[8]),
                  "x": 179.5,
                  "y": 113,
                  "wires": [["A59272376e6026c"]]},
                 {"id": "Ad780a0d2d4a09",
                  "type": "multi actuate",
                  "z": "A37b7b487ab5cac",
                  "name": "Raspberry Pi",
                  "device_source": "self",
                  "devices_source_dynamic": "",
                  "devices_source_dynamicFieldType": "msg",
                  "devices_source_configured": [""],
                  "attrs": "command",
                  "_devices_loaded": True,
                  "x": 572.5,
                  "y": 286,
                  "wires": []},
                 {"id": "A59272376e6026c",
                  "type": "change",
                  "z": "A37b7b487ab5cac",
                  "name": "command",
                  "rules":
                      [{"t": "set",
                        "p": "command.message",
                        "pt": "msg",
                        "to": "OK!",
                        "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 371.5,
                  "y": 205,
                  "wires": [["Ad780a0d2d4a09"]]}
                 ]
        })

        flows.append({
            "name": "Publish FTP",
            "enabled": True,
            "id": "2a6511dc-8ad1-4a58-ab42-213281d63d3f",
            "flow":
                [{"id": "81f229c7.c43d88", "type": "tab", "label": "Fluxo 1"},
                 {"id": "1644ae1e.ca0d72",
                  "type": "template",
                  "z": "81f229c7.c43d88",
                  "name": "data filename",
                  "field": "data_filename",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{{payload.data.attrs.band}}-{{payloadMetadata.timestamp}}.txt",
                  "output": "str",
                  "x": 615.5,
                  "y": 194.5,
                  "wires": [["A267e55b35e43da", "A63f30d36d4f454"]]},
                 {"id": "dfbec05a.9604c8",
                  "type": "template",
                  "z": "81f229c7.c43d88",
                  "name": "image filename",
                  "field": "image_filename",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{{payload.data.attrs.band}}-{{payloadMetadata.timestamp}}-01.jpg",
                  "output": "str",
                  "x": 199,
                  "y": 194,
                  "wires": [["7526eed9.4b4c98"]]},
                 {"id": "7526eed9.4b4c98",
                  "type": "template",
                  "z": "81f229c7.c43d88",
                  "name": "data content",
                  "field": "data_content",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "datahora: {{payloadMetadata.timestamp}}\nfaixa: {{payload.data.attrs.band}}\nplaca: {{payload.data.attrs.license_plate}}\ncoordenadas: {{payload.data.attrs.coordinates}}\nclassificacao: {{payload.data.attrs.vehicle_type}}\nimagens: {{image_filename}}",
                  "output": "str",
                  "x": 406.5,
                  "y": 193.5,
                  "wires": [["1644ae1e.ca0d72"]]},
                 {"id": "Abfe0a08f78ae6",
                  "type": "event template in",
                  "z": "81f229c7.c43d88",
                  "name": "",
                  "event_create": False,
                  "event_update": False,
                  "event_remove": False,
                  "event_configure": False,
                  "event_publish": True,
                  "template_id": str(template_ids[8]),
                  "x": 178.5,
                  "y": 77,
                  "wires": [["dfbec05a.9604c8"]]},
                 {"id": "A267e55b35e43da",
                  "type": "publish-ftp",
                  "z": "81f229c7.c43d88",
                  "name": "",
                  "encode": "base64",
                  "filename": "image_filename",
                  "filecontent": "payload.data.attrs.image",
                  "x": 846.5,
                  "y": 301,
                  "wires": []},
                 {"id": "A63f30d36d4f454",
                  "type": "publish-ftp",
                  "z": "81f229c7.c43d88",
                  "name": "",
                  "encode": "utf8",
                  "filename": "data_filename",
                  "filecontent": "data_content",
                  "x": 750.5,
                  "y": 429,
                  "wires": []}]
        })

        flows.append({
            "name": "Publish FTP - Qualcomm",
            "enabled": True,
            "id": "2a6511dc-8ad1-4a58-ab42-213281d63d3f",
            "flow":
                [{"id": "81f229c7.c43d88", "type": "tab", "label": "Fluxo 1"},
                 {"id": "1644ae1e.ca0d72",
                  "type": "template",
                  "z": "81f229c7.c43d88",
                  "name": "data filename",
                  "field": "data_filename",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{{payload.data.attrs.band}}-{{payloadMetadata.timestamp}}.txt",
                  "output": "str",
                  "x": 615.5,
                  "y": 194.5,
                  "wires": [["A267e55b35e43da", "A63f30d36d4f454"]]},
                 {"id": "dfbec05a.9604c8",
                  "type": "template",
                  "z": "81f229c7.c43d88",
                  "name": "image filename",
                  "field": "image_filename",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{{payload.data.attrs.band}}-{{payloadMetadata.timestamp}}-01.jpg",
                  "output": "str",
                  "x": 199,
                  "y": 194,
                  "wires": [["7526eed9.4b4c98"]]},
                 {"id": "7526eed9.4b4c98",
                  "type": "template",
                  "z": "81f229c7.c43d88",
                  "name": "data content",
                  "field": "data_content",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "datahora: {{payloadMetadata.timestamp}}\nfaixa: {{payload.data.attrs.band}}\nplaca: {{payload.data.attrs.license_plate}}\ncoordenadas: {{payload.data.attrs.coordinates}}\nclassificacao: {{payload.data.attrs.vehicle_type}}\nimagens: {{image_filename}}",
                  "output": "str",
                  "x": 406.5,
                  "y": 193.5,
                  "wires": [["1644ae1e.ca0d72"]]},
                 {"id": "Abfe0a08f78ae6",
                  "type": "event template in",
                  "z": "81f229c7.c43d88",
                  "name": "",
                  "event_create": False,
                  "event_update": False,
                  "event_remove": False,
                  "event_configure": False,
                  "event_publish": True,
                  "template_id": str(template_ids[14]),
                  "x": 178.5,
                  "y": 77,
                  "wires": [["dfbec05a.9604c8"]]},
                 {"id": "A267e55b35e43da",
                  "type": "publish-ftp",
                  "z": "81f229c7.c43d88",
                  "name": "",
                  "encode": "base64",
                  "filename": "image_filename",
                  "filecontent": "payload.data.attrs.image",
                  "x": 846.5,
                  "y": 301,
                  "wires": []},
                 {"id": "A63f30d36d4f454",
                  "type": "publish-ftp",
                  "z": "81f229c7.c43d88",
                  "name": "",
                  "encode": "utf8",
                  "filename": "data_filename",
                  "filecontent": "data_content",
                  "x": 750.5,
                  "y": 429,
                  "wires": []}]
        })

        flows.append({
            "name": "http - JSON",
            "flow": [
                {"id": "A16db3ac1cf89b5", "type": "tab", "label": "Fluxo 1"},
                {"id": "Ab547a5bc1e8158",
                 "type": "event template in",
                 "z": "A16db3ac1cf89b5",
                 "name": "",
                 "event_create": False,
                 "event_update": False,
                 "event_remove": False,
                 "event_configure": False,
                 "event_publish": True,
                 "template_id": str(template_ids[12]),
                 "x": 135,
                 "y": 87,
                 "wires": [["Acaa9d000d0413"]]},
                {"id": "A49eda1cf521b6",
                 "type": "http",
                 "z": "A16db3ac1cf89b5",
                 "name": "",
                 "method": "POST",
                 "ret": "obj",
                 "body": "request",
                 "response": "resposta",
                 "url": "http://192.168.0.38:8000/auth",
                 "x": 326.5,
                 "y": 275,
                 "wires": [["A19c5db5e70f325", "Ae552a4998e3438"]]},
                {"id": "Acaa9d000d0413",
                 "type": "template",
                 "z": "A16db3ac1cf89b5",
                 "name": "",
                 "field": "request",
                 "fieldType": "msg",
                 "syntax": "handlebars",
                 "template": "{\n\"headers\": {\n\"content-type\": \"application/json\"\n},\n\"payload\": {\n\"username\":\"{{payload.data.attrs.username}}\",\n\"passwd\":\"{{payload.data.attrs.passwd}}\"\n}\n}",
                 "output": "str",
                 "x": 226.5,
                 "y": 171,
                 "wires": [["A49eda1cf521b6"]]},
                {"id": "A2781b54821c09a",
                 "type": "multi device out",
                 "z": "A16db3ac1cf89b5",
                 "name": "",
                 "device_source": "configured",
                 "devices_source_dynamic": "",
                 "devices_source_dynamicFieldType": "msg",
                 "devices_source_configured": [Api.get_deviceid_by_label(jwt, 'token')],
                 "attrs": "saida",
                 "_devices_loaded": True,
                 "x": 872.5,
                 "y": 272,
                 "wires": []},
                {"id": "A19c5db5e70f325",
                 "type": "change",
                 "z": "A16db3ac1cf89b5",
                 "name": "",
                 "rules":
                     [{"t": "set",
                       "p": "saida.jwt",
                       "pt": "msg",
                       "to": "resposta.payload.jwt",
                       "tot": "msg"}],
                 "action": "",
                 "property": "",
                 "from": "",
                 "to": "",
                 "reg": False,
                 "x": 585,
                 "y": 341,
                 "wires": [["A2781b54821c09a"]]},
                {"id": "Ae552a4998e3438",
                 "type": "change",
                 "z": "A16db3ac1cf89b5",
                 "name": "",
                 "rules":
                     [{"t": "set",
                       "p": "saida.json",
                       "pt": "msg",
                       "to": "resposta.payload",
                       "tot": "msg"}],
                 "action": "",
                 "property": "",
                 "from": "",
                 "to": "",
                 "reg": False,
                 "x": 565,
                 "y": 200,
                 "wires": [["A2781b54821c09a"]]}]
        })

        flows.append({
            "name": "outros eventos",
            "flow":
                [{"id": "Ae2d39a3bb2c5d8", "type": "tab", "label": "Flow 1"},
                 {"id": "A9fae5ee670405",
                  "type": "event template in",
                  "z": "Ae2d39a3bb2c5d8",
                  "name": "Ônibus",
                  "event_create": True,
                  "event_update": False,
                  "event_remove": False,
                  "event_configure": False,
                  "event_publish": False,
                  "template_id": str(template_ids[5]),
                  "x": 117.5,
                  "y": 104,
                  "wires": [["A33548f1f78fd7"]]},
                 {"id": "A33548f1f78fd7",
                  "type": "change",
                  "z": "Ae2d39a3bb2c5d8",
                  "name": "criação",
                  "rules":
                      [{"t": "set",
                        "p": "saida.mensagem",
                        "pt": "msg",
                        "to": "criação de dispositivo",
                        "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 342.5,
                  "y": 103,
                  "wires": [["A97d86eb6bc7b4"]]},
                 {"id": "A97d86eb6bc7b4",
                  "type": "multi device out",
                  "z": "Ae2d39a3bb2c5d8",
                  "name": "",
                  "device_source": "configured",
                  "devices_source_dynamic": "",
                  "devices_source_dynamicFieldType": "msg",
                  "devices_source_configured": [Api.get_deviceid_by_label(jwt, 'controle')],
                  "attrs": "saida",
                  "_devices_loaded": True,
                  "x": 638.5,
                  "y": 246,
                  "wires": []},
                 {"id": "Ad33f9d23ee20f",
                  "type": "event template in",
                  "z": "Ae2d39a3bb2c5d8",
                  "name": "Ônibus",
                  "event_create": False,
                  "event_update": True,
                  "event_remove": False,
                  "event_configure": False,
                  "event_publish": False,
                  "template_id": str(template_ids[5]),
                  "x": 121,
                  "y": 197,
                  "wires": [["Aaf5c594907ad38"]]},
                 {"id": "A7cb8815c51a78",
                  "type": "event template in",
                  "z": "Ae2d39a3bb2c5d8",
                  "name": "Ônibus",
                  "event_create": False,
                  "event_update": False,
                  "event_remove": True,
                  "event_configure": False,
                  "event_publish": False,
                  "template_id": str(template_ids[5]),
                  "x": 127,
                  "y": 282,
                  "wires": [["Ae2a247921a0f48"]]},
                 {"id": "A4349de0e26d1b",
                  "type": "event template in",
                  "z": "Ae2d39a3bb2c5d8",
                  "name": "Ônibus",
                  "event_create": False,
                  "event_update": False,
                  "event_remove": False,
                  "event_configure": True,
                  "event_publish": False,
                  "template_id": str(template_ids[5]),
                  "x": 132,
                  "y": 386,
                  "wires": [["A5c0b2ae7b70634"]]},
                 {"id": "Aaf5c594907ad38",
                  "type": "change",
                  "z": "Ae2d39a3bb2c5d8",
                  "name": "atualização",
                  "rules":
                      [{"t": "set",
                        "p": "saida.mensagem",
                        "pt": "msg",
                        "to": "atualização de dispositivo",
                        "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 362,
                  "y": 196,
                  "wires": [["A97d86eb6bc7b4"]]},
                 {"id": "Ae2a247921a0f48",
                  "type": "change",
                  "z": "Ae2d39a3bb2c5d8",
                  "name": "remoção",
                  "rules":
                      [{"t": "set",
                        "p": "saida.mensagem",
                        "pt": "msg",
                        "to": "remoção de dispositivo",
                        "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 357,
                  "y": 282,
                  "wires": [["A97d86eb6bc7b4"]]},
                 {"id": "A5c0b2ae7b70634",
                  "type": "change",
                  "z": "Ae2d39a3bb2c5d8",
                  "name": "atuação",
                  "rules":
                      [{"t": "set",
                        "p": "saida.mensagem",
                        "pt": "msg",
                        "to": "atuação no dispositivo",
                        "tot": "str"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 365,
                  "y": 386,
                  "wires": [["A97d86eb6bc7b4"]]}]
        })

        flows.append({
            "name": "notificacao - sem persistencia",
            "flow":
                [{"id": "ea21ed04.e04c9", "type": "tab", "label": "Flow 1"},
                 {"id": "6971025a.64948c",
                  "type": "event template in",
                  "z": "ea21ed04.e04c9",
                  "name": "TesteTemplate",
                  "event_create": False,
                  "event_update": False,
                  "event_remove": False,
                  "event_configure": False,
                  "event_publish": True,
                  "template_id": str(template_ids[7]),
                  "x": 117.94790649414062,
                  "y": 133.1840362548828,
                  "wires": [["91cde1ab.a5e9e"]]},
                 {"id": "91cde1ab.a5e9e",
                  "type": "switch",
                  "z": "ea21ed04.e04c9",
                  "name": "int >= 0",
                  "property": "payload.data.attrs.int",
                  "propertyType": "msg",
                  "rules": [{"t": "gte", "v": "0", "vt": "num"}],
                  "checkall": "true",
                  "outputs": "1",
                  "x": 282.94798278808594,
                  "y": 207.43401908874512,
                  "wires": [["4395ba8.454c144"]]},
                 {"id": "d708a3a6.a6735",
                  "type": "notification",
                  "z": "ea21ed04.e04c9",
                  "name": "notificação",
                  "source": "persistencia",
                  "sourceFieldType": "msg",
                  "messageDynamic": "notification.message",
                  "messageStatic": "",
                  "messageFieldType": "msg",
                  "msgType": "dynamic",
                  "x": 749.9514770507812,
                  "y": 507.30218505859375,
                  "wires": [[]]},
                 {"id": "4395ba8.454c144",
                  "type": "template",
                  "z": "ea21ed04.e04c9",
                  "name": "",
                  "field": "notification",
                  "fieldType": "msg",
                  "syntax": "handlebars",
                  "template": "{\"message\":\"notificação não é persistida\",\n\"metadata\":{\"prioridade\":\"baixa\"}\n}",
                  "output": "json",
                  "x": 389.9549255371094,
                  "y": 298.4236145019531,
                  "wires": [["Ab7202043e4c2"]]},
                 {"id": "Ab7202043e4c2",
                  "type": "change",
                  "z": "ea21ed04.e04c9",
                  "name": "",
                  "rules":
                      [{"t": "set",
                        "p": "persistencia.shouldPersist",
                        "pt": "msg",
                        "to": "false",
                        "tot": "bool"}],
                  "action": "",
                  "property": "",
                  "from": "",
                  "to": "",
                  "reg": False,
                  "x": 628.5,
                  "y": 433,
                  "wires": [["d708a3a6.a6735"]]}]
        })

        flows_ids = self.createFlows(jwt, flows)

        self.logger.info("Flows created. IDs: " + str(flows_ids))

        # group1 = {"name": "viewer" + str(random.randint(0, 100)),
        #           "description": "Grupo com acesso somente para visualizar as informações"}
        # rc, response = Api.create_group(jwt, group1)
        # self.logger.debug(f"Group group1 creation return the result code: {rc} and response: {response}")
        # self.assertTrue(int(rc) == 200, "Error on create group")
        # group1_id = response["id"]

        # self.logger.info("Groups created. IDs: " + str(group1_id))

        # #TODO adicionar as permissoes ao grupo

        # rc, res = Api.add_permission(jwt, group1_id, "2")
        # self.logger.info("Permissions added to the group: " + str(group1_id))
        # self.assertTrue(int(rc) == 200, "codigo inesperado")

        # rc, res = Api.add_permission(jwt, group1_id, "4")
        # self.logger.info("Permissions added to the group: " + str(group1_id))
        # self.assertTrue(int(rc) == 200, "codigo inesperado")

        # rc, res = Api.add_permission(jwt, group1_id, "6")
        # self.logger.info("Permissions added to the group: " + str(group1_id))
        # self.assertTrue(int(rc) == 200, "codigo inesperado")

        # adicionar usuario

        # user1 = {"username": "bete",
        #     "service": "teste",
        #     "email": "bete@noemail.com",
        #     "name": "Elisabete",
        #     "profile": "admin"
        #     }
        # self.createUsers(jwt, user1)
        # self.logger.info("User created: bete")

        # user2 = {
        #     "username": "maria",
        #     "service": "teste",
        #     "email": "maria@noemail.com",
        #     "name": "Maria",
        #     "profile": "admin"
        #     }
        # self.createUsers(jwt, user2)
        # self.logger.info("User created: maria")

        # TODO listar tenants

        # publicações

        dev1_id = Api.get_deviceid_by_label(jwt, "linha_1")
        dev1_topic = "admin:" + dev1_id + "/attrs"
        dev1 = MQTTClient(dev1_id)
        self.logger.info("publicando com dispositivo: " + dev1_id)
        dev1.publish(dev1_topic,
                     {"gps": "-22.890970, -47.063006", "velocidade": 50, "passageiros": 30, "operacional": False})
        time.sleep(1)
        dev1.publish(dev1_topic,
                     {"gps": "-22.893619, -47.052921", "velocidade": 40, "passageiros": 45, "operacional": True})
        time.sleep(5)

        dev2_id = Api.get_deviceid_by_label(jwt, "dispositivo")
        dev2_topic = "admin:" + dev2_id + "/attrs"
        dev2 = MQTTClient(dev2_id)
        self.logger.info("publicando com dispositivo: " + dev2_id)
        dev2.publish(dev2_topic, {"int": 2})

        # TODO: obter histórico do dev1_id

        Api.get_history_device(jwt, dev1_id)

        time.sleep(1)

        # TODO: obter histórico do dev2_id

        Api.get_history_device(jwt, dev2_id)

        time.sleep(1)

        dev_id = Api.get_deviceid_by_label(jwt, "anemometro")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"velocidade": 50})

        time.sleep(2)

        dev_id = Api.get_deviceid_by_label(jwt, "barometro")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"pressao": 0.9})

        time.sleep(2)

        dev_id = Api.get_deviceid_by_label(jwt, "higrometro")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"umidade": 15})

        time.sleep(2)

        dev_id = Api.get_deviceid_by_label(jwt, "termometro Celsius")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"temperatura": 30})

        time.sleep(2)

        dev_id = Api.get_deviceid_by_label(jwt, "device")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"bool": True})

        time.sleep(5)

        dev_id = Api.get_deviceid_by_label(jwt, "dispositivo")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"bool": True})

        time.sleep(5)

        dev_id = Api.get_deviceid_by_label(jwt, "Pluviometro")

        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"chuva": 5})

        time.sleep(3)

        dev.publish(dev_topic, {"chuva": 6})

        time.sleep(3)

        dev.publish(dev_topic, {"chuva": 10})

        time.sleep(3)

        dev_id = Api.get_deviceid_by_label(jwt, "SensorNivel")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"nivel": 1})

        time.sleep(3)

        dev.publish(dev_topic, {"nivel": 2.1})

        time.sleep(3)

        dev.publish(dev_topic, {"nivel": 2.6})

        time.sleep(3)

        dev_id = Api.get_deviceid_by_label(jwt, "device")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"int": 1})

        time.sleep(2)

        """

        dev_id = Api.get_deviceid_by_label(jwt, "Camera1")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {})
        # mosquitto_pub -h ${HOST_MQTT} -p ${PORT_MQTT} -t ${tenant}:${id_device}/attrs -u ${tenant}:${id_device}  -f  ./arquivo.jpg.txt 2>/dev/null

        time.sleep(10)
        
        dev_id = Api.get_deviceid_by_label(jwt, "CameraQualcomm")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {})
        # mosquitto_pub -h ${HOST_MQTT} -p ${PORT_MQTT} -t ${tenant}:${id_device}/attrs -u ${tenant}:${id_device}  -f  ./arquivo.jpg.qualcomm.txt 2>/dev/null

        time.sleep(10)
        """

        dev_id = Api.get_deviceid_by_label(jwt, "acesso")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"username": "admin", "passwd": "admin"})

        time.sleep(2)

        dev_id = Api.get_deviceid_by_label(jwt, "linha_2")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"velocidade": 60})

        time.sleep(2)

        dev_id = Api.get_deviceid_by_label(jwt, "device")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"int": 2})

        time.sleep(2)

        dev_id = Api.get_deviceid_by_label(jwt, "higrometro")
        dev_topic = "admin:" + dev_id + "/attrs"
        dev = MQTTClient(dev_id)
        self.logger.info("publicando com dispositivo: " + dev_id)
        dev.publish(dev_topic, {"umidade": 12})

        time.sleep(2)

        # create device linha_4
        Api.create_device(jwt, [template_ids[5]], "linha_4")

        # update device linha_4
        # delete device linha_4
