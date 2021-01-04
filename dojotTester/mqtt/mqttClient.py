import paho.mqtt.client as mqtt
from config import CONFIG
from utils import Utils
import json

LOGGER = Utils.create_logger("mqtt_client")

class MQTTClient:
    """
    MQTT client to Dojot MQTT IoTAgent.
    """
    def __init__(self,
                 device_id: str
                 ):
        """
        MQTT client constructor. To get this to work, you should call setup() after instantiating
        the class.

        Args:
            device_id: device identifier
        """
        LOGGER.debug("initiating mqtt client device " + device_id)
        mqtt_keepalive = 60
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        #client.tls_set(ca_certs=ca_certificate, certfile=client_certificate, keyfile=client_key)
        # client.tls_insecure_set(1)
        self.client.username_pw_set(CONFIG['app']['tenant'] + ":" + device_id)
        self.client.connect(host=CONFIG['mqtt']['host'], port=CONFIG['mqtt']['port'], keepalive=mqtt_keepalive)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        LOGGER.info("Result from connect: {}".format(mqtt.connack_string(rc)))
        # Subscribe to the vehicles/vehiclepi01/tests topic filter
        # client.subscribe("vehicles/vehiclepi01/tests", qos=2)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        LOGGER.info("I've subscribed with QoS: {}".format(granted_qos[0]))

    def on_message(self, client, userdata, msg):
        LOGGER.info("Message received. Topic: {}. Payload: {}".format(msg.topic, str(msg.payload)))

    def publish(self, topic, payload):
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        self.client.publish(topic, payload)
