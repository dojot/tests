"""
API calls to Dojot.
"""
import json
from typing import Callable, List, Dict
import requests
import gevent

from config import CONFIG
from utils import Utils


LOGGER = Utils.create_logger("api")


class APICallError(Exception):
    """
    Error when trying to call Dojot API.
    """


class DojotAPI():
    """
    Utility class with API calls to Dojot.
    """
    @staticmethod
    def get_jwt() -> str:
        """
        Request a JWT token.
        """
        LOGGER.debug("Retrieving JWT...")

        args = {
            "url": "{0}/auth".format(CONFIG['dojot']['url']),
            "data": json.dumps({
                "username": CONFIG['dojot']['user'],
                "passwd": CONFIG['dojot']['passwd'],
            }),
            "headers": {
                "Content-Type": "application/json"
            },
        }

        _, res = DojotAPI.call_api(requests.post, args)

        LOGGER.debug(".. retrieved JWT")
        return res["jwt"]

    @staticmethod
    def create_devices(jwt: str, template_id: str, total: int, batch: int) -> None:
        """
        Create the devices.

        Parameters:
            jwt: Dojot JWT token
            template_id: template ID to be used by the devices
            n: total number of devices to be created
            batch: number of devices to be created in each iteration
        """
        LOGGER.debug("Creating devices...")

        args = {
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
        }

        loads = DojotAPI.divide_loads(total, batch)

        for i, load in enumerate(loads):
            args["data"] = json.dumps({
                "templates": [template_id],
                "attrs": {},
                "label": "CargoContainer_{0}".format(i)
            })
            args["url"] = "{0}/device?count={1}&verbose=false".format(CONFIG['dojot']['url'], load)

            DojotAPI.call_api(requests.post, args)

        LOGGER.debug("... created the devices")

    @staticmethod
    def create_template(jwt: str, data=None) -> str:
        """
        Create the default template for test devices.

        Returns the created template ID or a error message.
        """
        LOGGER.debug("Creating template...")
        if data is None:
            data = json.dumps({
                "label": "dummy template",
                "attrs": [
                    {
                        "label": "timestamp",
                        "type": "dynamic",
                        "value_type": "integer"
                    },
                ]
            })
        if isinstance(data, dict):
            data = json.dumps(data)

        args = {
            "url": "{0}/template".format(CONFIG['dojot']['url']),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
            "data": data,
        }

        result_code, res = DojotAPI.call_api(requests.post, args)

        LOGGER.debug("... created the template")
        return result_code, res["template"]["id"] if result_code==200 else res

    @staticmethod
    def create_device(jwt: str, template_id: str, label: str) -> str:
        """
        Create a device in Dojot.

        Parameters:
            jwt: JWT authorization.
            template_id: template to be used by the device.
            label: name for the device in Dojot.

        Returns the created device ID or a error message.
        """
        LOGGER.debug("Creating device...")

        if type(template_id) != list:
            template_id = [template_id]

        args = {
            "url": "{0}/device".format(CONFIG['dojot']['url']),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
            "data": json.dumps({
                "templates": template_id,
                "attrs": {},
                "label": label,
            }),
        }

        result_code, res = DojotAPI.call_api(requests.post, args)

        LOGGER.debug("... device created ")
        return result_code, res["devices"][0]["id"] if result_code == 200 else res

    @staticmethod
    def create_flow(jwt: str, flow: str) -> str:
        """
        Create a flow in Dojot.

        Parameters:
            jwt: JWT authorization.
            flow: flow definition.


        Returns the created flow ID.
        """
        LOGGER.debug("Creating flow...")

        args = {
            "url": "{0}/flows/v1/flow".format(CONFIG['dojot']['url']),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
            "data": json.dumps(flow),
        }

        result_code, res = DojotAPI.call_api(requests.post, args)

        LOGGER.debug("... flow created")
        return result_code, res["flow"]["id"] if result_code == 200 else res

    @staticmethod
    def create_group(jwt: str, group: str) -> str: ##Tuple[Any, Any]:
        """
        Create a group in Dojot.

        Parameters:
            jwt: JWT authorization.
            group: group definition.


        Returns the created group ID.
        """
        LOGGER.debug("Creating group...")

        args = {
            "url": "{0}/auth/pap/group".format(CONFIG['dojot']['url']),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
            "data": json.dumps(group),
        }

        result_code, res = DojotAPI.call_api(requests.post, args)


        LOGGER.debug("... group created")

        ## o retorno do comando é: {"status": 200, "id": 6}. Como obter só o ID?

        return result_code, res["id"] if result_code == 200 else res

    @staticmethod
    def add_permission(jwt: str, group: str, permission: str) -> str:
        """
        Add permission a group in Dojot.

        Parameters:
            jwt: JWT authorization.
            group: group receiving permission
            permission: permission definition


        Returns the created group ID.
        """
        LOGGER.debug("Adding permission...")

        args = {
            "url": "{0}/auth/pap/grouppermissions/{1}/{2}".format(CONFIG['dojot']['url'], group, permission),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
        }

        result_code, res = DojotAPI.call_api(requests.post, args)

        LOGGER.debug("... permission added")
        return result_code, res["message"] if result_code == 200 else res

    @staticmethod
    def create_user(jwt: str, user: str) -> str:
        """
        Create a user in Dojot.

        Parameters:
            jwt: JWT authorization.
            user: user data.


        Returns the created user ID.
        """
        LOGGER.debug("Creating user...")

        args = {
            "url": "{0}/auth/user".format(CONFIG['dojot']['url']),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
            "data": json.dumps(user),
        }

        result_code, res = DojotAPI.call_api(requests.post, args)

        LOGGER.debug("... user created")
        return result_code, res if result_code == 200 else res

    @staticmethod
    def get_deviceid_by_label(jwt: str, label: str) -> str:
        """
        Retrieves the devices from Dojot.

        Parameters:
            jwt: Dojot JWT token

        Returns a list of IDs.
        """
        LOGGER.debug("Retrieving devices...")

        args = {
            "url": "{0}/device?idsOnly=true&label={1}".format(CONFIG['dojot']['url'], label),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
        }

        rc, res = DojotAPI.call_api(requests.get, args)

        devices_id = res[0] if rc == 200 else None

        LOGGER.debug("... retrieved the devices")

        return devices_id

    @staticmethod
    def get_templateid_by_label(jwt: str, label: str) -> str:
        """
        Retrieves the template from Dojot.

        Parameters:
            jwt: Dojot JWT token

        Returns a template ID
        """
        #FIXME
        LOGGER.debug("Retrieving template...")

        args = {
            "url": "{0}/template?label={1}".format(CONFIG['dojot']['url'], label),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
        }

        rc, res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... retrieved the template id")
        return res["attrs"]["template_id"] if rc == 200 else res


    @staticmethod
    def update_template(jwt: str, template_id: int, data: str) -> str:
        """

        Returns the updated template ID or a error message.
        """
        LOGGER.debug("Updating template...")

        if isinstance(data, dict):
            data = json.dumps(data)

        args = {
            "url": "{0}/template/{1}".format(CONFIG['dojot']['url'], template_id),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
            "data": data,
        }

        result_code, res = DojotAPI.call_api(requests.put, args)

        LOGGER.debug("... updated the template")
        return result_code, res if result_code==200 else res



    @staticmethod
    def delete_devices(jwt: str) -> None:
        """
        Delete all devices.
        """
        # FIXME
        LOGGER.debug("Deleting devices...")

        args = {
            "url": "{0}/device".format(CONFIG['dojot']['url']),
            "headers": {
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        DojotAPI.call_api(requests.delete, args)

        LOGGER.debug("... deleted devices")

    @staticmethod
    def delete_device(jwt: str, label: str) -> None:
        """
        Delete device.
        """
        # FIXME
        LOGGER.debug("Deleting device...")

        args = {
            "url": "{0}/device/{1}".format(CONFIG['dojot']['url'], label),
            "headers": {
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        DojotAPI.call_api(requests.delete, args)

        LOGGER.debug("... deleted device")

    @staticmethod
    def delete_templates(jwt: str) -> None:
        """
        Delete all templates.
        """
        # FIXME
        LOGGER.debug("Deleting templates...")

        args = {
            "url": "{0}/template".format(CONFIG['dojot']['url']),
            "headers": {
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        DojotAPI.call_api(requests.delete, args)

        LOGGER.debug("... deleted templates")

    @staticmethod
    def get_devices(jwt: str) -> List:
        """
        Retrieves the devices from Dojot.

        Parameters:
            jwt: Dojot JWT token

        Returns a list of IDs.
        """
        # FIXME
        LOGGER.debug("Retrieving devices...")

        args = {
            "url": "{0}/device".format(CONFIG['dojot']['url']),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        res = DojotAPI.call_api(requests.get, args)

        devices_ids = [device['id'] for device in res['devices']]

        LOGGER.debug("... retrieved the devices")

        return devices_ids


    @staticmethod
    def get_templates(jwt: str) -> str:
        """
        Retrieves all templates.

        Parameters:
            jwt: Dojot JWT token

            """
        LOGGER.debug("Retrieving templates...")

        args = {
            "url": "{0}/template".format(CONFIG['dojot']['url']),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... retrieved all templates")

        return res

    @staticmethod
    def get_templates_with_parameters(jwt: str, attrs: str) -> str:
        """
        Retrieves all templates.

        Parameters:
            jwt: Dojot JWT token
            attrs: optional parameters

            """
        LOGGER.debug("Retrieving templates...")

        args = {
            "url": "{0}/template?{1}".format(CONFIG['dojot']['url'], attrs),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... retrieved all templates")

        return res


    @staticmethod
    def get_template(jwt: str, template_id: int) -> str:
        """
        Retrieves all information from a specific template

        Parameters:
            jwt: Dojot JWT token

            """
        LOGGER.debug("Retrieving information from a specific template...")

        args = {
            "url": "{0}/template/{1}".format(CONFIG['dojot']['url'], template_id),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... retrieved information from a specific template")

        return res

    @staticmethod
    def get_history_device(jwt: str, label: str) -> str:
        """
        Retrieves device attributes data from Dojot.

        Parameters:
            jwt: Dojot JWT token

            """
        LOGGER.debug("Retrieving history...")

        args = {
            "url": "{0}/history/device/{1}/history".format(CONFIG['dojot']['url'], label),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... retrieved history")

        return res


    @staticmethod
    def divide_loads(total: int, batch: int) -> List:
        """
        Divides `n` in a list with each element being up to `batch`.
        """
        # FIXME
        loads = []

        if total > batch:
            iterations = total // batch
            exceeding = total % batch
            # This will create a list with the number `batch` repeated `iterations` times
            # and then `exceeding` at the final
            loads = [batch] * iterations
            if exceeding > 0:
                loads.append(exceeding)

        else:
            loads.append(total)

        return loads

    @staticmethod
    def call_api(func: Callable[..., requests.Response], args: dict) -> Dict:
        """
        Calls the Dojot API using `func` and `args`.

        Parameters:
            func: function to call Dojot API.
            args: dictionary of arguments to `func`

        Returns the response in a dictionary
        """
        for _ in range(CONFIG['dojot']['api']['retries'] + 1):
            try:
                res = func(**args)
                #res.raise_for_status()

            except Exception as exception:
                LOGGER.debug(str(exception))
                gevent.sleep(CONFIG['dojot']['api']['time'])

            else:
                return res.status_code, res.json()

        raise APICallError("exceeded the number of retries to {0}".format(args['url']))
