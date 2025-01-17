import logging

from .pi30 import pi30

log = logging.getLogger("pi41")

# New / overriden commands
NEW_COMMANDS = {
    "QP2GS": {
        "name": "QP2GS",
        "description": "Parallel Information inquiry",
        "help": " -- example: QP2GS1 queries the values of various metrics from instance 1 of parallel setup Inverters (numbers from 0)",
        "type": "QUERY",
        "response": [
            ["int", "Parallel instance number??", ""],
            ["int", "Serial number", ""],
            [
                "keyed",
                "Work mode",
                {
                    "P": "Power On Mode",
                    "S": "Standby Mode",
                    "L": "Line Mode",
                    "B": "Battery Mode",
                    "F": "Fault Mode",
                    "H": "Power Saving Mode",
                },
            ],
            [
                "keyed",
                "Fault code",
                {
                    "00": "No fault",
                    "01": "Fan is locked",
                    "02": "Over temperature",
                    "03": "Battery voltage is too high",
                    "04": "Battery voltage is too low",
                    "05": "Output short circuited or Over temperature",
                    "06": "Output voltage is too high",
                    "07": "Over load time out",
                    "08": "Bus voltage is too high",
                    "09": "Bus soft start failed",
                    "11": "Main relay failed",
                    "51": "Over current inverter",
                    "52": "Bus soft start failed",
                    "53": "Inverter soft start failed",
                    "54": "Self-test failed",
                    "55": "Over DC voltage on output of inverter",
                    "56": "Battery connection is open",
                    "57": "Current sensor failed",
                    "58": "Output voltage is too low",
                    "60": "Inverter negative power",
                    "71": "Parallel version different",
                    "72": "Output circuit failed",
                    "80": "CAN communication failed",
                    "81": "Parallel host line lost",
                    "82": "Parallel synchronized signal lost",
                    "83": "Parallel battery voltage detect different",
                    "84": "Parallel Line voltage or frequency detect different",
                    "85": "Parallel Line input current unbalanced",
                    "86": "Parallel output setting different",
                },
            ],
            ["float", "L2 AC input voltage", "V"],
            ["float", "L2 AC input frequency", "Hz"],
            ["float", "L2 AC output voltage", "V"],
            ["float", "L2 AC output frequency", "Hz"],
            ["int", "L2 AC output apparent power", "VA"],
            ["int", "L2 AC output active power", "W"],
            ["int", "L2 Load percentage", "%"],
            ["float", "L2 Battery voltage", "V"],
            ["int", "L2 Battery charging current", "A"],
            ["int", "L2 Battery capacity", "%"],
            ["float", "PV2 Input Voltage", "V"],
            ["int", "PV2 charging current", "A"],
            [
                "flags",
                "Inverter Status",
                [
                    "is_l2_scc_ok",
                    "is_l2_ac_charging",
                    "is_l2_scc_charging",
                    "is_battery_over_voltage",
                    "is_battery_under_voltage",
                    "is_l2_line_lost",
                    "is_l2_load_on",
                    "is_configuration_changed",
                ],
            ],
        ],
        "test_responses": [
            b"(11 92911906100045 L 00 124.2 59.98 124.2 59.98 0149 0130 005 56.1 000 100 000.0 00 01000010\xA9\xA8\r",
        ],
        "regex": "QP2GS(\\d)$",
    },
    "QPGS": {
        "name": "QPGS",
        "description": "Parallel Information inquiry LV5048",
        "help": " -- example: QPGS1 queries the values of various metrics from instance 1 of parallel setup Inverters (numbers from 0)",
        "type": "QUERY",
        "response": [
            ["option", "Parallel instance number", ["Not valid", "valid"]],
            ["int", "Serial number", ""],
            [
                "keyed",
                "Work mode",
                {
                    "P": "Power On Mode",
                    "S": "Standby Mode",
                    "L": "Line Mode",
                    "B": "Battery Mode",
                    "F": "Fault Mode",
                    "H": "Power Saving Mode",
                },
            ],
            [
                "keyed",
                "Fault code",
                {
                    "00": "No fault",
                    "01": "Fan is locked",
                    "02": "Over temperature",
                    "03": "Battery voltage is too high",
                    "04": "Battery voltage is too low",
                    "05": "Output short circuited or Over temperature",
                    "06": "Output voltage is too high",
                    "07": "Over load time out",
                    "08": "Bus voltage is too high",
                    "09": "Bus soft start failed",
                    "11": "Main relay failed",
                    "51": "Over current inverter",
                    "52": "Bus soft start failed",
                    "53": "Inverter soft start failed",
                    "54": "Self-test failed",
                    "55": "Over DC voltage on output of inverter",
                    "56": "Battery connection is open",
                    "57": "Current sensor failed",
                    "58": "Output voltage is too low",
                    "60": "Inverter negative power",
                    "71": "Parallel version different",
                    "72": "Output circuit failed",
                    "80": "CAN communication failed",
                    "81": "Parallel host line lost",
                    "82": "Parallel synchronized signal lost",
                    "83": "Parallel battery voltage detect different",
                    "84": "Parallel Line voltage or frequency detect different",
                    "85": "Parallel Line input current unbalanced",
                    "86": "Parallel output setting different",
                },
            ],
            ["float", "L1 AC input voltage", "V"],
            ["float", "L1 AC input frequency", "Hz"],
            ["float", "L1 AC output voltage", "V"],
            ["float", "L1 AC output frequency", "Hz"],
            ["int", "L1 AC output apparent power", "VA"],
            ["int", "L1 AC output active power", "W"],
            ["int", "L1 Load percentage", "%"],
            ["float", "Battery voltage", "V"],
            ["int", "Battery charging current", "A"],
            ["int", "Battery capacity", "%"],
            ["float", "PV1 Input Voltage", "V"],
            ["int", "Total charging current", "A"],
            ["int", "Total AC output apparent power", "VA"],
            ["int", "Total output active power", "W"],
            ["int", "Total AC output percentage", "%"],
            [
                "flags",
                "Inverter Status",
                [
                    "is_l1_scc_ok",
                    "is_l1_ac_charging_on",
                    "is_l1_scc_charging_on",
                    "is_battery_over_voltage",
                    "is_battery_under_voltage",
                    "is_l1_line_off",
                    "is_l1_load_on",
                    "is_configuration_changed",
                ],
            ],
            [
                "option",
                "Output mode",
                [
                    "Standalone?",
                    "Parallel output 0 degrees",
                    "Phase 1 of 3 Phase output",
                    "Phase 2 of 3 Phase output",
                    "Phase 3 of 3 Phase output",
                    "Parallel output 120 degrees",
                    "Parallel output 180 degrees",
                ],
            ],
            [
                "option",
                "Charger source priority",
                ["Utility first", "Solar first", "Solar + Utility", "Solar only"],
            ],
            ["int", "Max charger current", "A"],
            ["int", "Max charger range", "A"],
            ["int", "Max AC charger current", "A"],
            ["int", "PV1 charging current", "A"],
            ["int", "Battery discharge current", "A"],
        ],
        "test_responses": [
            b"(1 92911906100045 L 00 122.9 59.98 122.9 59.98 0331 0272 013 56.1 004 100 000.0 004 01577 01400 009 01000010 6 0 060 220 40 00 000\xC7\xC2\r",
        ],
        "regex": "QPGS(\\d)$",
    },
    "QPIGS": {
        "name": "QPIGS",
        "description": "General Status Parameters inquiry LV5048",
        "help": " -- queries the value of various metrics from the Inverter",
        "type": "QUERY",
        "response": [
            ["float", "L1 AC Input Voltage", "V"],
            ["float", "L1 AC Input Frequency", "Hz"],
            ["float", "L1 AC Output Voltage", "V"],
            ["float", "L1 AC Output Frequency", "Hz"],
            ["int", "L1 AC Output Apparent Power", "VA"],
            ["int", "L1 AC Output Active Power", "W"],
            ["int", "L1 AC Output Load", "%"],
            ["int", "BUS Voltage", "V"],
            ["float", "Battery Voltage", "V"],
            ["int", "Battery Charging Current", "A"],
            ["int", "Battery Capacity", "%"],
            ["int", "Inverter Heat Sink Temperature", "Deg_C"],
            ["float", "PV Input Current for Battery", "A"],
            ["float", "PV Input Voltage", "V"],
            ["float", "Battery Voltage from SCC", "V"],
            ["int", "Battery Discharge Current", "A"],
            [
                "flags",
                "Inverter Status",
                [
                    "is_l1_scc_ok",
                    "is_l1_ac_charging_on",
                    "is_l1_scc_charging_on",
                    "is_battery_over",
                    "is_battery_under",
                    "is_l1_line_not_ok",
                    "is_load_on",
                    "is_configuration_changed",
                ],
            ],
            ["int", "RSV1", "A"],
            ["int", "RSV2", "A"],
            ["int", "PV Input Power", "W"],
            [
                "flags",
                "Device Status2",
                ["is_charging_to_float", "is_switched_on", "is_reserved"],
            ],
        ],
        "test_responses": [
            b"(000.0 00.0 230.0 49.9 0161 0119 003 460 57.50 012 100 0069 0014 103.8 57.45 00000 00110110 00 00 00856 010\x24\x8C\r",
        ],
    },
    "QPIGS2": {
        "name": "QPIGS2",
        "description": "General Status Parameters inquiry",
        "help": " -- queries the value of various metrics from the Inverter",
        "type": "QUERY",
        "response": [
            ["float", "L2 AC Input Voltage", "V"],
            ["float", "L2 AC Input Frequency", "Hz"],
            ["float", "L2 AC Output Voltage", "V"],
            ["float", "L2 AC Output Frequency", "Hz"],
            ["int", "L2 AC Output Apparent Power", "VA"],
            ["int", "L2 AC Output Active Power", "W"],
            ["int", "L2 AC Output Load", "%"],
            ["int", "PV2 Battery Charging Current", "A"],
            ["float", "PV2 Input Voltage", "V"],
            ["float", "L2 Battery Voltage", "V"],
            [
                "flags",
                "Device Status",
                [
                    "is_l2_scc_ok",
                    "is_l2_ac_charging_on",
                    "is_l2_scc_charging_on",
                    "reserved",
                    "is_l2_line_not_ok",
                    "is_load_on",
                    "reserved",
                ],
            ],
        ],
        "test_responses": [
            b"",
        ],
    },
    "QPIRI": {
        "name": "QPIRI",
        "description": "Current Settings inquiry for LV5048",
        "help": " -- queries the current settings from the Inverter",
        "type": "QUERY",
        "response": [
            ["float", "AC Input Voltage", "V"],
            ["float", "AC Input Current", "A"],
            ["float", "AC Output Voltage", "V"],
            ["float", "AC Output Frequency", "Hz"],
            ["float", "AC Output Current", "A"],
            ["int", "AC Output Apparent Power", "VA"],
            ["int", "AC Output Active Power", "W"],
            ["float", "Battery Voltage", "V"],
            ["float", "Battery Recharge Voltage", "V"],
            ["float", "Battery Under Voltage", "V"],
            ["float", "Battery Bulk Charge Voltage", "V"],
            ["float", "Battery Float Charge Voltage", "V"],
            ["option", "Battery Type", ["AGM", "Flooded", "User"]],
            ["int", "Max AC Charging Current", "A"],
            ["int", "Max Charging Current", "A"],
            ["option", "Input Voltage Range", ["Appliance", "UPS"]],
            [
                "option",
                "Output Source Priority",
                ["Utility first", "Solar first", "SBU first"],
            ],
            [
                "option",
                "Charger Source Priority",
                [
                    "Utility first",
                    "Solar first",
                    "Solar + Utility",
                    "Only solar charging permitted",
                ],
            ],
            ["int", "Max Parallel Units", "units"],
            [
                "keyed",
                "Machine Type",
                {"00": "Grid tie", "01": "Off Grid", "10": "Hybrid"},
            ],
            ["option", "Topology", ["transformerless", "transformer"]],
            [
                "option",
                "Output Mode",
                [
                    "Standalone?",
                    "Parallel output 0 degrees",
                    "Phase 1 of 3 Phase output",
                    "Phase 2 of 3 Phase output",
                    "Phase 3 of 3 Phase output",
                    "Parallel output 120 degrees",
                    "Parallel output 180 degrees",
                ],
            ],
            ["float", "Battery Redischarge Voltage", "V"],
            [
                "option",
                "PV OK Condition",
                [
                    "As long as one unit of inverters has connect PV, parallel system will consider PV OK",
                    "Only All of inverters have connect PV, parallel system will consider PV OK",
                ],
            ],
            [
                "option",
                "PV Power Balance",
                [
                    "PV input max current will be the max charged current",
                    "PV input max power will be the sum of the max charged power and loads power",
                ],
            ],
            ["int", "Max Charging Time at CV Stage", "min"],
        ],
        "test_responses": [
            b"(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1 60\x83\xAA\r",
            b"(120.0 20.8 120.0 60.0 20.8 2500 2500 48.0 47.0 43.0 56.1 56.1 2 40 060 0 0 0 9 01 0 6 55.0 0 1 000\xBE\xAC\r",
            b"(NAK\x73\x73\r",
        ],
    },
}


class pi41(pi30):
    def __str__(self):
        return "PI41 protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI41"
        self.COMMANDS.update(NEW_COMMANDS)
        self.STATUS_COMMANDS = ["QPIGS", "Q1"]
        self.SETTINGS_COMMANDS = ["QPIRI", "QFLAG"]
        self.DEFAULT_COMMAND = "QDI"
        # log.info(f'Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands')
