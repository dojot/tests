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
    def create_template(jwt: str, data=None or dict) -> tuple:
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
        return result_code, res

    @staticmethod
    def create_device(jwt: str, template_id: str or list, label: str) -> tuple:
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
        return result_code, res

    @staticmethod
    def create_flow(jwt: str, flow: str) -> tuple:
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
        return result_code, res

    @staticmethod
    def create_group(jwt: str, group: str) -> tuple:
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

        return result_code, res

    @staticmethod
    def add_permission(jwt: str, group: str, permission: str) -> tuple:
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
        return result_code, res

    @staticmethod
    def create_user(jwt: str, user: str) -> tuple:
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
        return result_code, res

    @staticmethod
    def get_deviceid_by_label(jwt: str, label: str) -> str or None:
        """
        Retrieves the devices from Dojot.

        Parameters:
            jwt: Dojot JWT token
            label: Dojot device label

        Returns device ID or None.
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
    def update_template(jwt: str, template_id: int, data: str) -> tuple:
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
        return result_code, res


    @staticmethod
    def delete_devices(jwt: str) -> tuple:
        """
        Delete all devices.
        """
        LOGGER.debug("Deleting devices...")

        args = {
            "url": "{0}/device".format(CONFIG['dojot']['url']),
            "headers": {
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        rc, res = DojotAPI.call_api(requests.delete, args)

        LOGGER.debug("... deleted devices")
        return rc, res


    @staticmethod
    def delete_device(jwt: str, device_id: str) -> tuple:
        """
        Delete device.
        """
        LOGGER.debug("Deleting device...")

        args = {
            "url": "{0}/device/{1}".format(CONFIG['dojot']['url'], device_id),
            "headers": {
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        rc, res = DojotAPI.call_api(requests.delete, args)

        LOGGER.debug("... deleted device")
        return rc, res

    @staticmethod
    def delete_templates(jwt: str) -> tuple:
        """
        Delete all templates.
        """
        LOGGER.debug("Deleting templates...")

        args = {
            "url": "{0}/template".format(CONFIG['dojot']['url']),
            "headers": {
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        rc, res = DojotAPI.call_api(requests.delete, args)

        LOGGER.debug("... deleted templates")

        return rc, res


    @staticmethod
    def delete_template(jwt: str, template_id: int) -> tuple:
        """
        Delete specific template.
        """

        LOGGER.debug("Deleting template...")

        args = {
            "url": "{0}/template/{1}".format(CONFIG['dojot']['url'], str(template_id)),
            "headers": {
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        rc, res = DojotAPI.call_api(requests.delete, args)

        LOGGER.debug("... deleted template")
        return rc, res

    @staticmethod
    def get_devices(jwt: str) -> List:
        """
        Retrieves the devices from Dojot.

        Parameters:
            jwt: Dojot JWT token

        Returns a list of IDs.
        """
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
    def get_templates(jwt: str) -> tuple:
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

        rc, res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... retrieved all templates")

        return rc, res

    @staticmethod
    def get_templates_with_parameters(jwt: str, attrs: str) -> tuple:
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

        rc, res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... retrieved all templates")

        return rc, res


    @staticmethod
    def get_template(jwt: str, template_id: int) -> tuple:
        """
        Retrieves all information from a specific template

        Parameters:
            jwt: Dojot JWT token

            """
        LOGGER.debug("Retrieving information from a specific template...")

        args = {
            "url": "{0}/template/{1}".format(CONFIG['dojot']['url'], str(template_id)),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        rc, res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... retrieved information from a specific template")

        return rc, res

    @staticmethod
    def get_template_with_parameters(jwt: str, template_id: int, attrs: str) -> tuple:
        """
        Retrieves template info.

        Parameters:
            jwt: Dojot JWT token
            attrs: optional parameters

            """
        LOGGER.debug("Retrieving template...")

        args = {
            "url": "{0}/template/{1}?{2}".format(CONFIG['dojot']['url'], str(template_id), attrs),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        rc, res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... retrieved template")

        return rc, res

    @staticmethod
    def create_devices_with_parameters(jwt: str, template_id: str or list, label: str, attrs: str) -> tuple:
        """
        Create a device in Dojot.

        Parameters:
            jwt: JWT authorization.
            template_id: template to be used by the device.
            label: name for the device in Dojot.

        Returns the created device ID or a error message.
        """
        LOGGER.debug("Creating multiple devices...")

        if type(template_id) != list:
            template_id = [template_id]

        args = {
            "url": "{0}/device?{1}".format(CONFIG['dojot']['url'], attrs),
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

        LOGGER.debug("... devices created ")
        return result_code, res


    @staticmethod
    def get_all_devices(jwt: str) -> tuple:
        """
        Retrieves all devices in Dojot.

        Parameters:
            jwt: JWT authorization.

        Returns the created device ID or a error message.
        """
        LOGGER.debug("Listing all devices...")

        args = {
            "url": "{0}/device".format(CONFIG['dojot']['url']),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        result_code, res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... devices created ")
        return result_code, res


    @staticmethod
    def get_single_device(jwt: str, device_id: str) -> tuple:
        """
        Retrieves a device in Dojot.

        Parameters:
            jwt: JWT authorization.

        Returns the created device ID or a error message.
        """
        LOGGER.debug("Listing device info...")

        args = {
            "url": "{0}/device/{1}".format(CONFIG['dojot']['url'], device_id),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        result_code, res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... device retrieved ")
        return result_code, res

    @staticmethod
    def get_devices_with_parameters(jwt: str, attrs: str) -> tuple:
        """
        Retrieves all templates.

        Parameters:
            jwt: Dojot JWT token
            attrs: optional parameters

            """
        LOGGER.debug("Retrieving devices...")

        args = {
            "url": "{0}/device{1}".format(CONFIG['dojot']['url'], attrs),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        rc, res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("...devices retrieved")

        return rc, res


    @staticmethod
    def update_device(jwt: str, device_id: str, data: str or dict) -> tuple:
        """

        Returns the updated device ID or a error message.
        """
        LOGGER.debug("Updating device...")

        if isinstance(data, dict):
            data = json.dumps(data)
        args = {
            "url": "{0}/device/{1}".format(CONFIG['dojot']['url'], device_id),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
            "data": data,
        }

        result_code, res = DojotAPI.call_api(requests.put, args)

        LOGGER.debug("... updated the device")
        return result_code, res


    @staticmethod
    def get_history_device(jwt: str, label: str) -> tuple:
        """
        Retrieves device attributes data from Dojot.

        Parameters:
            jwt: Dojot JWT token
            label: Dojot device label

            """
        LOGGER.debug("Retrieving history...")

        args = {
            "url": "{0}/history/device/{1}/history".format(CONFIG['dojot']['url'], label),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            }
        }

        rc, res = DojotAPI.call_api(requests.get, args)

        LOGGER.debug("... retrieved history")

        return rc, res

    @staticmethod
    def configure_device(jwt: str, device_id: str, data: str or dict) -> tuple:
        """

        Returns the configured device or a error message.
        """
        LOGGER.debug("configuring device...")

        if isinstance(data, dict):
            data = json.dumps(data)
        args = {
            "url": "{0}/device/{1}/actuate".format(CONFIG['dojot']['url'], device_id),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(jwt),
            },
            "data": data,
        }

        result_code, res = DojotAPI.call_api(requests.put, args)

        LOGGER.debug("... configured device")
        return result_code, res



    @staticmethod
    def divide_loads(total: int, batch: int) -> List:
        """
        Divides `n` in a list with each element being up to `batch`.
        """
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
