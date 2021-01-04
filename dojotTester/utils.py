"""
Utils functions.
"""
import logging
import os



LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


class Utils():
    """Project Utils class."""

    @staticmethod
    def log_level(level_name: str) -> int:
        """
        Parses the log level and returns the correct values for the logging package.

        Args:
            level_name: wanted log level.

        Returns the value that the logging package understands, defaults to INFO.
        """
        level_name = level_name.lower()

        return LOG_LEVELS[level_name] if LOG_LEVELS.get(level_name) else LOG_LEVELS["info"]

    @staticmethod
    def validate_device_id(device_id: str) -> None:
        """
        Validates the device ID.

        Raises a ValueError when the ID is invalid.
        """
        if len(device_id) < 1:
            raise ValueError("the device ID must have at least one character")

    @staticmethod
    def validate_tenant(tenant: str) -> None:
        """
        Validates the tenant.

        Raises a ValueError when the tenant is invalid.
        """
        if len(tenant) < 1:
            raise ValueError("the tenant name must have at least one character")

    @staticmethod
    def validate_thing_id(thing_id: str) -> None:
        """
        Validates a thing ID. Its format must be tenant:deviceid.

        Raises a ValueError when the thing ID is invalid.
        """
        split = thing_id.split(":")

        if len(split) != 2:
            raise ValueError("the thing ID must be in the format tenant:deviceid")

        Utils.validate_tenant(split[0])
        Utils.validate_device_id(split[1])

    @staticmethod
    def create_thing_id(tenant: str, device_id: str) -> str:
        """
        Create the thing ID.
        """
        Utils.validate_tenant(tenant)
        Utils.validate_device_id(device_id)

        return f"{tenant}:{device_id}"

    @staticmethod
    def seconds_to_milliseconds(time: float) -> int:
        """
        Converts seconds to milliseconds.

        Params:
            time: time in seconds to be converted.
        """
        return int(time * 1000.0)


    @staticmethod
    def create_logger(name: str = "root") -> logging.Logger:
        """
        Create a Logger instance with the configs passed via config.py.

        Params:
            name: name of the logger
        """
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(name)s line %(lineno)s | %(asctime)s [%(levelname)s]: %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(Utils.log_level(os.environ.get("LOG_LEVEL", "info")))

        return logger
