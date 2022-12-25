import importlib
import logging
import pkgutil

from mppsolar.outputs import (
    baseoutput,
    domoticz_autodiscover,
    domoticz_mqtt,
    hass_mqtt,
    hassd_mqtt,
    influx2_mqtt,
    influx_mqtt,
    json,
    json_mqtt,
    json_udp,
    mqtt,
    raw,
    screen,
    tag_mqtt,
)

LOG = logging.getLogger(__name__)

OUTPUTS = {
    "baseoutput": baseoutput.BaseOutput,
    "domoticz_autodiscover": domoticz_autodiscover.DomoticzAutodiscover,
    "domoticz_mqtt": domoticz_mqtt.DomoticzMQTT,
    "hass_mqtt": hass_mqtt.HassMQTT,
    "hassd_mqtt": hassd_mqtt.HassdMQTT,
    "influx_mqtt": influx_mqtt.InfluxMQTT,
    "influx2_mqtt": influx2_mqtt.Influx2MQTT,
    "json_mqtt": json_mqtt.JsonMQTT,
    "json": json.Json,
    "raw": raw.Raw,
    "tag_mqtt": tag_mqtt.TagMQTT,
    "json_udp": json_udp.JsonUDP,
    "mqtt": mqtt.MQTT,
    "screen": screen.Screen,
}


def list_outputs():
    pkgpath = __file__
    pkgpath = pkgpath[: pkgpath.rfind("/")]
    pkgpath += "/../outputs"
    result = {}
    result["_command"] = "outputs help"
    result["_command_description"] = "List available output modules"
    for _, name, _ in pkgutil.iter_modules([pkgpath]):
        try:
            _module_class = importlib.import_module("mppsolar.outputs." + name, ".")
            _module = getattr(_module_class, name)
            result[name] = (str(_module()), "", "")
        except ModuleNotFoundError as e:
            LOG.error(f"Error in module {name}: {e}")
    return result


def get_output(output):
    """
    Take an output name
    attempt to find and instantiate the corresponding module
    """
    LOG.info("Attempting to create output processor: %s", output)
    output_cls = OUTPUTS.get(output)
    if output_cls is None:
        LOG.critical("No module found for output processor %s", output)
        return None
    else:
        return output_cls()


def get_outputs(output_list):
    """
    Take a comma separated list of output names
    attempt to find and instantiate the corresponding module
    return array of modules
    """
    ops = []
    outputs = output_list.split(",")
    for output in outputs:
        op = get_output(output)
        if op is not None:
            ops.append(op)
    return ops


def output_results(results, outputs, mqtt_broker):
    LOG.info("outputs: %s", outputs)

    for op in outputs:
        # maybe include the command and what the command is im the output
        # eg QDI run, Display Inverter Default Settings
        # filter_ = config.get("CONFIG", "filter")
        # log.debug(f"Using output filter: {filter}")
        output = get_output(op["name"])
        output.output(
            data=dict(results),
            # tag=config.get("CONFIG", "tag"),
            mqtt_broker=mqtt_broker,
            # filter=filter,
            # excl_filter=excl_filter,
            # keep_case=keep_case,
        )
