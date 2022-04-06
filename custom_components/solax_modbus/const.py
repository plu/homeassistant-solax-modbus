from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntityDescription,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)

from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_CURRENT_MILLIAMPERE,
    ELECTRIC_POTENTIAL_VOLT,
    ENERGY_KILO_WATT_HOUR,
    ENERGY_MEGA_WATT_HOUR,
    FREQUENCY_HERTZ,
    PERCENTAGE,
    POWER_VOLT_AMPERE,
    POWER_WATT,
    TEMP_CELSIUS,
    TIME_HOURS,
)


""" ============================================================================================
bitmasks  definitions to characterize inverters, ogranized by group
these bitmasks are used in entitydeclarations to determine to which inverters the entity applies
within a group, the bits in an entitydeclaration will be interpreted as OR
between groups, an AND condition is applied, so all gruoups must match """

GEN_GROUP_BITS = 0x00FF # inverter generation bits
GEN2             = 0x0002
GEN3             = 0x0004
GEN4             = 0x0008

X13_GROUP_BITS = 0x0300 # X1 or X3 model flags
X1               = 0x0100
X3               = 0x0200

HYB_GROUP_BITS = 0x0C000 # hybrid or AC flags
HYBRID           = 0x0400
AC               = 0x0800

EPS_GROUP_BITS = 0x1000  # EPS flag
EPS              = 0x1000


ALLDEFAULT = HYBRID | AC | GEN2 | GEN3 | GEN4 | X1 | X3 # maybe need to remove AC from default


def matchInverterWithMask (inverterspec, entitymask):
    # returns true if the entity needs to be created for an inverter
    genmatch = ((inverterspec & entitymask & GEN_GROUP_BITS) != 0) or (entitymask & GEN_GROUP_BITS == 0)
    xmatch   = ((inverterspec & entitymask & X13_GROUP_BITS) != 0) or (entitymask & X13_GROUP_BITS == 0)
    hybmatch = ((inverterspec & entitymask & HYB_GROUP_BITS) != 0) or (entitymask & HYB_GROUP_BITS == 0)
    epsmatch = ((inverterspec & entitymask & EPS_GROUP_BITS) != 0) or (entitymask & EPS_GROUP_BITS == 0)
    return genmatch and xmatch and hybmatch and epsmatch

"""
end of bitmask handling code
==============================================================================================="""


DOMAIN = "solax_modbus"
DEFAULT_NAME = "SolaX"
DEFAULT_SCAN_INTERVAL = 15
DEFAULT_PORT = 502
DEFAULT_MODBUS_ADDR = 1
CONF_READ_GEN2X1 = "read_gen2_x1"
CONF_READ_GEN3X1 = "read_gen3_x1"
CONF_READ_GEN3X3 = "read_gen3_x3"
CONF_READ_GEN4X1 = "read_gen4_x1"
CONF_READ_GEN4X3 = "read_gen4_x3"
CONF_READ_X1_EPS = "read_x1_eps"
CONF_READ_X3_EPS = "read_x3_eps"
CONF_MODBUS_ADDR = "read_modbus_addr"
CONF_SERIAL      = "read_serial"
CONF_SERIAL_PORT = "read_serial_port"
CONF_SolaX_HUB   = "solax_hub"
ATTR_MANUFACTURER = "SolaX Power"
DEFAULT_SERIAL      = False
DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_READ_GEN2X1 = False
DEFAULT_READ_GEN3X1 = False
DEFAULT_READ_GEN3X3 = False
DEFAULT_READ_GEN4X1 = False
DEFAULT_READ_GEN4X3 = False
DEFAULT_READ_X1_EPS = False
DEFAULT_READ_X3_EPS = False

BUTTON_TYPES = [
    ["Battery Awaken",
        "battery_awaken",
        0x56,
        1,
    ],
    ["Unlock Inverter",
        "unlock_inverter",
        0x00,
        2014,
    ],
]

NUMBER_TYPES = []

NUMBER_TYPES_G2 = [
        ["Battery Minimum Capacity",
            "battery_minimum_capacity",
            0x20,
            "i",
            {
                "min": 0,
                "max": 99,
                "step": 1,
                "unit": PERCENTAGE,
            },
            "battery_capacity_charge"
        ],
	["Battery Charge Max Current",
	    "battery_charge_max_current",
	    0x24,
	    "f",
	    {
               "min": 0,
               "max": 50,
               "step": 0.1,
               "unit": ELECTRIC_CURRENT_AMPERE,
            }
	],
        ["Battery Discharge Max Current",
            "battery_discharge_max_current",
            0x25,
            "f",
           {
                "min": 0,
                "max": 50,
                "step": 0.1,
                "unit": ELECTRIC_CURRENT_AMPERE,
            }
        ],
]
NUMBER_TYPES_G3 = [
        ["Battery Minimum Capacity",
            "battery_minimum_capacity",
            0x20,
            "i",
            {
               "min": 0,
                "max": 99,
                "step": 1,
                "unit": PERCENTAGE,
            },
            "battery_capacity_charge"
        ],
        ["Battery Charge Max Current",
	        "battery_charge_max_current",
	        0x24,
	        "f",
            {
                "min": 0,
                "max": 20,
                "step": 0.1,
                "unit": ELECTRIC_CURRENT_AMPERE,
            }
        ],
        ["Battery Discharge Max Current",
            "battery_discharge_max_current",
            0x25,
            "f",
            {
                "min": 0,
                "max": 20,
                "step": 0.1,
                "unit": ELECTRIC_CURRENT_AMPERE,
            }
        ],
        ["ForceTime Period 1 Max Capacity",
            "forcetime_period_1_max_capacity",
            0xA4,
            "i",
            {
                "min": 5,
                "max": 100,
                "step": 1,
                "unit": PERCENTAGE,
            }
         ],
        ["ForceTime Period 2 Max Capacity",
            "forcetime_period_2_max_capacity",
            0xA5,
            "i",
            {
                "min": 5,
                "max": 100,
                "step": 1,
                "unit": PERCENTAGE,
            }
        ],
]
NUMBER_TYPES_G4 = [
        ["Battery Charge Max Currrent",
            "battery_charge_max_current",
            0x24,
            "f",
            {
                "min": 0,
                "max": 25,
                "step": 0.1,
                "unit": ELECTRIC_CURRENT_AMPERE,
            }
        ],
        ["Battery Discharge Max Current",
            "battery_discharge_max_current",
            0x25,
            "f",
            {
                "min": 0,
                "max": 25,
                "step": 0.1,
                "unit": ELECTRIC_CURRENT_AMPERE,
            }
        ],
        ["Export Control User Limit",
            "export_control_user_limit", 
            0x42,
            "i",
            {
                "min": 0,
                "max": 60000,
                "step": 500,
                "unit": POWER_WATT,
            }
        ],
        ["Selfuse Discharge Min SOC",
            "selfuse_discharge_min_soc",
            0x61,
            "i",
            {
                "min": 10,
                "max": 100,
                "step": 1,
                "unit": PERCENTAGE,
            }
        ],
        ["Selfuse Nightcharge Upper SOC",
            "selfuse_nightcharge_upper_soc", 
            0x63,
            "i",
            {
                "min": 10,
                "max": 100,
                "step": 1,
                "unit": PERCENTAGE,
            }
        ],
        ["Feedin Nightcharge Upper SOC",
            "feedin_nightcharge_upper_soc", 
            0x64,
            "i",
            {
                "min": 10,
                "max": 100,
                "step": 1,
                "unit": PERCENTAGE,
            }
         ],
         ["Feedin Discharge Min SOC",
            "feedin_discharge_min_soc",
            0x65,
            "i",
            {
                "min": 10,
                "max": 100,
                "step": 1,
                "unit": PERCENTAGE,
            }
        ],
        ["Backup Nightcharge Upper SOC",
            "backup_nightcharge_upper_soc", 
            0x66,
            "i",
            {
                "min": 10,
                "max": 100,
                "step": 1,
                "unit": PERCENTAGE,
            }
        ],
        ["Backup Discharge Min SOC",
            "backup_discharge_min_soc",
            0x67,
            "i",
            {
                "min": 10,
                "max": 100,
                "step": 1,
                "unit": PERCENTAGE,
            }
        ]
]

TIME_OPTIONS = {
    0: "00:00",
    3840: "00:15",
    7680: "00:30",
    11520: "00:45",
    1: "01:00",
    3841: "01:15",
    7681: "01:30",
    11521: "01:45",
    2: "02:00",
    3842: "02:15",
    7682: "02:30",
    11522: "02:45",
    3: "03:00",
    3843: "03:15",
    7683: "03:30",
    11523: "03:45",
    4: "04:00",
    3844: "04:15",
    7684: "04:30",
    11524: "04:45",
    5: "05:00",
    3845: "05:15",
    7685: "05:30",
    11525: "05:45",
    6: "06:00",
    3846: "06:15",
    7686: "06:30",
    11526: "06:45",
    7: "07:00",
    3847: "07:15",
    7687: "07:30",
    11527: "07:45",
    8: "08:00",
    3848: "08:15",
    7688: "08:30",
    11528: "08:45",
    9: "09:00",
    3849: "09:15",
    7689: "09:30",
    11529: "09:45",
    10: "10:00",
    3850: "10:15",
    7690: "10:30",
    11530: "10:45",
    11: "11:00",
    3851: "11:15",
    7691: "11:30",
    11531: "11:45",
    12: "12:00",
    3852: "12:15",
    7692: "12:30",
    11532: "12:45",
    13: "13:00",
    3853: "13:15",
    7693: "13:30",
    11533: "13:45",
    14: "14:00",
    3854: "14:15",
    7694: "14:30",
    11534: "14:45",
    15: "15:00",
    3855: "15:15",
    7695: "15:30",
    11535: "15:45",
    16: "16:00",
    3856: "16:15",
    7696: "16:30",
    11536: "16:45",
    17: "17:00",
    3857: "17:15",
    7697: "17:30",
    11537: "17:45",
    18: "18:00",
    3858: "18:15",
    7698: "18:30",
    11538: "18:45",
    19: "19:00",
    3859: "19:15",
    7699: "19:30",
    11539: "19:45",
    20: "20:00",
    3860: "20:15",
    7700: "20:30",
    11540: "20:45",
    21: "21:00",
    3861: "21:15",
    7701: "21:30",
    11541: "21:45",
    22: "22:00",
    3862: "22:15",
    7702: "22:30",
    11542: "22:45",
    23: "23:00",
    3863: "23:15",
    7703: "23:30",
    11543: "23:45", 
    15127: "23:59", # default value for Gen4 discharger_end_time_1 , maybe not a default for Gen2,Gen3
}

TIME_OPTIONS_GEN4 = { 
    0: "00:00",
    15: "00:15",
    30: "00:30",
    45: "00:45",
    256: "01:00",
    271: "01:15",
    286: "01:30",
    301: "01:45",
    512: "02:00",
    527: "02:15",
    542: "02:30",
    557: "02:45",
    768: "03:00",
    783: "03:15",
    798: "03:30",
    813: "03:45",
    1024: "04:00",
    1039: "04:15",
    1054: "04:30",
    1069: "04:45",
    1280: "05:00",
    1295: "05:15",
    1310: "05:30",
    1325: "05:45",
    1536: "06:00",
    1551: "06:15",
    1566: "06:30",
    1581: "06:45",
    1792: "07:00",
    1807: "07:15",
    1822: "07:30",
    1837: "07:45",
    2048: "08:00",
    2063: "08:15",
    2078: "08:30",
    2093: "08:45",
    2304: "09:00",
    2319: "09:15",
    2334: "09:30",
    2349: "09:45",
    2560: "10:00",
    2575: "10:15",
    2590: "10:30",
    2605: "10:45",
    2816: "11:00",
    2831: "11:15",
    2846: "11:30",
    2861: "11:45",
    3072: "12:00",
    3087: "12:15",
    3132: "12:30",
    3117: "12:45",
    3328: "13:00",
    3343: "13:15",
    3358: "13:30",
    3373: "13:45",
    3584: "14:00",
    3599: "14:15",
    3614: "14:30",
    3629: "14:45",
    3840: "15:00",
    3855: "15:15",
    3870: "15:30",
    3885: "15:45",
    4096: "16:00",
    4111: "16:15",
    4126: "16:30",
    4141: "16:45",
    4352: "17:00",
    4367: "17:15",
    4382: "17:30",
    4397: "17:45",
    4608: "18:00",
    4623: "18:15",
    4638: "18:30",
    4653: "18:45",
    4864: "19:00",
    4879: "19:15",
    4894: "19:30",
    4909: "19:45",
    5120: "20:00",
    5135: "20:15",
    5150: "20:30",
    5165: "20:45",
    5376: "21:00",
    5391: "21:15",
    5406: "21:30",
    5421: "21:45",
    5632: "22:00",
    5647: "22:15",
    5662: "22:30",
    5677: "22:45",
    5888: "23:00",
    5903: "23:15",
    5918: "23:30",
    5933: "23:45",
    5947: "23:59", # default value for discharger_end_time1
}



SELECT_TYPES = [
	["Charger Use Mode",
	    "charger_use_mode",
	    0x1F,
	    {
	        0: "Self Use Mode",
            1: "Force Time Use",
            2: "Back Up Mode",
            3: "Feedin Priority",
        }
	],
        ["Allow Grid Charge",
            "allow_grid_charge",
            0x40,
            {
                0: "Both Forbidden",
                1: "Period 1 Allowed",
                2: "Period 2 Allowed",
                3: "Both Allowed",
            }
        ],
	["Charger Start Time 1",
	    "charger_start_time_1",
	    0x26,
	    TIME_OPTIONS
	],
	["Charger End Time 1",
	    "charger_end_time_1",
	    0x27,
	    TIME_OPTIONS
	],
	["Charger Start Time 2",
	    "charger_start_time_2",
	    0x2A,
	    TIME_OPTIONS
	],
	["Charger End Time 2",
	    "charger_end_time_2",
	    0x2B,
	    TIME_OPTIONS
	],
	["Discharger Start Time 1",
	    "discharger_start_time_1",
	    0x28,
	    TIME_OPTIONS
	],
	["Discharger End Time 1",
	    "discharger_end_time_1",
	    0x29,
	    TIME_OPTIONS
	],
	["Discharger Start Time 2",
	    "discharger_start_time_2",
	    0x2C,
	    TIME_OPTIONS
	],
	["Discharger End Time 2",
	    "discharger_end_time_2",
	    0x2D,
	    TIME_OPTIONS
	],
]

SELECT_TYPES_G4 = [
	["Charger Use Mode",
	    "charger_use_mode",
	    0x1F,
            {
                0: "Self Use Mode",
                1: "Feedin Priority",
                2: "Back Up Mode",
                3: "Manual Mode",
            }
        ],
        ["Manual Mode Select",
            "manual_mode",
            0x20,
            {   0: "Stop Charge and Discharge",
                1: "Force Charge",
                2: "Force Discharge",
            }
        ],
        ["Selfuse Night Charge Enable",
            "selfuse_nightcharge_enable",
            0x62,
            {   0: "Disabled",
                1: "Enabled",
            }
        ],
        ["Charge and Discharge Period2 Enable",
            "charge_period2_enable",
            0x6C,
            {   0: "Disabled",
                1: "Enabled",
            }
        ],
        [   "Charger Start Time 1",
            "charger_start_time_1",
            0x68,
            TIME_OPTIONS_GEN4
        ],
        [   "Charger End Time 1",
            "charger_end_time_1",
            0x69,
            TIME_OPTIONS_GEN4
        ],
        [   "Discharger Start Time 1",
            "discharger_start_time_1",
            0x6A,
            TIME_OPTIONS_GEN4
        ],
        [   "Discharger End Time 1",
            "discharger_end_time_1",
            0x6B,
            TIME_OPTIONS_GEN4
        ], 
        [   "Charger Start Time 2",
            "charger_start_time_2",
            0x6D,
            TIME_OPTIONS_GEN4
        ],
        [   "Charger End Time 2",
            "charger_end_time_2",
            0x6E,
            TIME_OPTIONS_GEN4
        ],
        [   "Discharger Start Time 2",
            "discharger_start_time_2",
            0x6F,
            TIME_OPTIONS_GEN4
        ],
        [   "Discharger End Time 2",
            "discharger_end_time_2",
            0x70,
            TIME_OPTIONS_GEN4
        ],
]

@dataclass
class SolaXModbusSensorEntityDescription(SensorEntityDescription):
    """A class that describes SolaX Power Modbus sensor entities."""
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 is a better choice



SENSOR_TYPES: dict[str, list[SolaXModbusSensorEntityDescription]] = {  
    "allow_grid_charge": SolaXModbusSensorEntityDescription(
        name="Allow Grid Charge",
        key="allow_grid_charge",
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT & ~GEN4,
    ),
    "battery_capacity_charge": SolaXModbusSensorEntityDescription(
    	name="Battery Capacity",
    	key="battery_capacity_charge",
    	native_unit_of_measurement=PERCENTAGE,
    	device_class=DEVICE_CLASS_BATTERY,
        allowedtypes=ALLDEFAULT, 
    ),
    "battery_charge_max_current": SolaXModbusSensorEntityDescription(
		name="Battery Charge Max Current",
		key="battery_charge_max_current",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        allowedtypes=ALLDEFAULT,
    ),
	"battery_current_charge": SolaXModbusSensorEntityDescription(
		name="Battery Current Charge",
		key="battery_current_charge",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes=ALLDEFAULT,
    ),
    "battery_dicharge_cut_off_voltage": SolaXModbusSensorEntityDescription(
		name="Battery Discharge Cut Off Voltage",
		key="battery_discharge_cut_off_voltage",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
	"battery_discharge_max_current": SolaXModbusSensorEntityDescription(
		name="Battery Discharge Max Current",
		key="battery_discharge_max_current",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
 	),
    "battery_minimum_capacity": SolaXModbusSensorEntityDescription(
    	name="Battery Minimum Capacity",
    	key="battery_minimum_capacity",
    	native_unit_of_measurement=PERCENTAGE,
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT & ~GEN4,
    ),
    "battery_package_number": SolaXModbusSensorEntityDescription(
    	name="Battery Package Number",
    	key="battery_package_number",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "battery_power_charge": SolaXModbusSensorEntityDescription(
    	name="Battery Power Charge",
    	key="battery_power_charge",
    	native_unit_of_measurement=POWER_WATT,
    	device_class=DEVICE_CLASS_POWER,
    	state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),
    "battery_soh": SolaXModbusSensorEntityDescription(
    	name="Battery State of Health",
    	key="battery_soh",
    	native_unit_of_measurement=PERCENTAGE,
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "battery_type": SolaXModbusSensorEntityDescription(
    	name="Battery Type",
    	key="battery_type",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "battery_charge_float_voltage": SolaXModbusSensorEntityDescription(
        name="Battery Charge Float Voltage",
        key="battery_charge_float_voltage",
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "battery_input_energy_charge": SolaXModbusSensorEntityDescription(
        name="Battery Input Energy",
        key="input_energy_charge",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "battery_output_energy_charge": SolaXModbusSensorEntityDescription(
        name="Battery Output Energy",
        key="output_energy_charge",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "battery_temperature": SolaXModbusSensorEntityDescription(
    	name="Battery Temperature",
    	key="battery_temperature",
    	native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),
	"battery_voltage_charge": SolaXModbusSensorEntityDescription(
		name="Battery Voltage Charge",
		key="battery_voltage_charge",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes=ALLDEFAULT,
    ),
    "battery_volt_fault_val": SolaXModbusSensorEntityDescription(
		name="Battery Volt Fault Val",
		key="battery_volt_fault_val",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
	"bms_charge_max_current": SolaXModbusSensorEntityDescription(
		name="BMS Charge Max Current",
		key="bms_charge_max_current",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
    "bms_connect_state": SolaXModbusSensorEntityDescription(
    	name="BMS Connect State", 
    	key="bms_connect_state",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "bms_discharge_max_current": SolaXModbusSensorEntityDescription(
		name="BMS Discharge Max Current",
		key="bms_discharge_max_current",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
	"bus_volt": SolaXModbusSensorEntityDescription(
		name="Bus Volt",
		key="bus_volt",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "charger_start_time_1": SolaXModbusSensorEntityDescription(
    	name="Charger Start Time 1",
    	key="charger_start_time_1",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "charger_end_time_1": SolaXModbusSensorEntityDescription(
    	name="Charger End Time 1",
    	key="charger_end_time_1",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "charger_start_time_2": SolaXModbusSensorEntityDescription(
    	name="Charger Start Time 2",
    	key="charger_start_time_2",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "charger_end_time_2": SolaXModbusSensorEntityDescription(
    	name="Charger End Time 2",
    	key="charger_end_time_2",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "charger_use_mode": SolaXModbusSensorEntityDescription(
    	name="Charger Use Mode",
    	key="charger_use_mode",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "grid_import_total": SolaXModbusSensorEntityDescription(
		name="Grid Import Total",
		key="grid_import_total",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "dc_fault_val": SolaXModbusSensorEntityDescription(
		name="DC Fault Val",
		key="dc_fault_val",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
	"discharger_start_time_1": SolaXModbusSensorEntityDescription(
    	name="Discharger Start Time 1",
    	key="discharger_start_time_1",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "discharger_end_time_1": SolaXModbusSensorEntityDescription(
    	name="Discharger End Time 1",
    	key="discharger_end_time_1",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "discharger_start_time_2": SolaXModbusSensorEntityDescription(
    	name="Discharger Start Time 2",
    	key="discharger_start_time_2",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "discharger_end_time_2": SolaXModbusSensorEntityDescription(
    	name="Discharger End Time 2",
    	key="discharger_end_time_2",
    	entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "today_yield": SolaXModbusSensorEntityDescription(
    	name="Today's Yield",
    	key="today_yield",
    	native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        allowedtypes=ALLDEFAULT,
    ),
    "export_control_factory_limit": SolaXModbusSensorEntityDescription(
		name="Export Control Factory Limit",
		key="export_control_factory_limit",
		native_unit_of_measurement=POWER_WATT,
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
	"export_control_user_limit": SolaXModbusSensorEntityDescription(
		name="Export Control User Limit",
		key="export_control_user_limit",
		native_unit_of_measurement=POWER_WATT,
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "grid_export_total": SolaXModbusSensorEntityDescription(
		name="Grid Export Total",
		key="grid_export_total",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "feedin_power": SolaXModbusSensorEntityDescription(
    	name="Measured Power",
    	key="feedin_power",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),
    "firmwareversion_invertermaster": SolaXModbusSensorEntityDescription(
		name="Firmware Version Inverter Master",
		key="firmwareversion_invertermaster",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
	"firmwareversion_manager": SolaXModbusSensorEntityDescription(
		name="Firmware Version Manager",
		key="firmwareversion_manager",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
	"firmwareversion_modbustcp_major": SolaXModbusSensorEntityDescription(
		name="Firmware Version Modbus TCP Major",
		key="firmwareversion_modbustcp_major",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
	"firmwareversion_modbustcp_minor": SolaXModbusSensorEntityDescription(
		name="Firmware Version Modbus TCP Minor",
		key="firmwareversion_modbustcp_minor",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
    "grid_frequency": SolaXModbusSensorEntityDescription(
    	name="Inverter Frequency",
    	key="grid_frequency",
    	native_unit_of_measurement=FREQUENCY_HERTZ,
        allowedtypes=ALLDEFAULT,
    ),
    "grid_import": SolaXModbusSensorEntityDescription(
    	name="Grid Import",
    	key="grid_import",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),
    "grid_export": SolaXModbusSensorEntityDescription(
    	name="Grid Export",
    	key="grid_export",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),
    "house_load": SolaXModbusSensorEntityDescription(
    	name="House Load",
    	key="house_load",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),    
    "inverter_voltage": SolaXModbusSensorEntityDescription(
    	name="Inverter Voltage",
    	key="inverter_voltage",
    	native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes=ALLDEFAULT,
    ),
    "inverter_current": SolaXModbusSensorEntityDescription(
    	name="Inverter Current",
    	key="inverter_current",
    	native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes=ALLDEFAULT,
    ),
    "inverter_load": SolaXModbusSensorEntityDescription(
    	name="Inverter Power",
    	key="inverter_load",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),
    "inverter_temperature": SolaXModbusSensorEntityDescription(
    	name="Inverter Temperature",
    	key="inverter_temperature",
    	native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),
    "language": SolaXModbusSensorEntityDescription(
		name="Language",
		key="language",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
	"lock_state": SolaXModbusSensorEntityDescription(
		name="Lock State",
		key="lock_state",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
    "bootloader_version": SolaXModbusSensorEntityDescription(
        name="Bootloader Version",
        key="bootloader_version",
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
	"modulename": SolaXModbusSensorEntityDescription(
		name="Module Name",
		key="modulename",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
	"normal_runtime": SolaXModbusSensorEntityDescription(
		name="Normal Runtime",
		key="normal_runtime",
		native_unit_of_measurement=TIME_HOURS,
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT & ~GEN4,
	),
	"overload_fault_val": SolaXModbusSensorEntityDescription(
		name="Overload Fault Val",
		key="overload_fault_val",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
    "pv_current_1": SolaXModbusSensorEntityDescription(
    	name="PV Current 1",
    	key="pv_current_1",
    	native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes=ALLDEFAULT,
    ),
    "pv_current_2": SolaXModbusSensorEntityDescription(
    	name="PV Current 2",
    	key="pv_current_2",
    	native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes=ALLDEFAULT,
    ),
    "pv_power_1": SolaXModbusSensorEntityDescription(
    	name="PV Power 1",
    	key="pv_power_1",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),
    "pv_power_2": SolaXModbusSensorEntityDescription(
    	name="PV Power 2",
    	key="pv_power_2",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),
    "pv_voltage_1": SolaXModbusSensorEntityDescription(
    	name="PV Voltage 1",
    	key="pv_voltage_1",
    	native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes=ALLDEFAULT,
    ),
    "pv_voltage_2": SolaXModbusSensorEntityDescription(
    	name="PV Voltage 2",
    	key="pv_voltage_2",
    	native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes=ALLDEFAULT,
    ),
    "pv_total_power": SolaXModbusSensorEntityDescription(
    	name="PV Total Power",
    	key="pv_total_power",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes=ALLDEFAULT,
    ),
    "registration_code": SolaXModbusSensorEntityDescription(
		name="Registration Code",
		key="registration_code",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT & ~GEN4,
	),
	"rtc": SolaXModbusSensorEntityDescription(
		name="RTC",
		key="rtc",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
    "run_mode": SolaXModbusSensorEntityDescription(
    	name="Run Mode",
    	key="run_mode",
        allowedtypes=ALLDEFAULT,
    ),
    "seriesnumber": SolaXModbusSensorEntityDescription(
		name="Series Number",
		key="seriesnumber",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
    "solar_energy_today": SolaXModbusSensorEntityDescription(
    	name="Today's Solar Energy",
    	key="solar_energy_today",
    	native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        allowedtypes=ALLDEFAULT,
    ),
    "solar_energy_total": SolaXModbusSensorEntityDescription(
    	name="Total Solar Energy",
    	key="solar_energy_total",
    	native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
        "e_charge_today": SolaXModbusSensorEntityDescription(
    	name="E Charge Today",
    	key="e_charge_today",
    	native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "e_charge_total": SolaXModbusSensorEntityDescription(
    	name="E Charge Total",
    	key="e_charge_total",
    	native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
    "time_count_down": SolaXModbusSensorEntityDescription(
		name="Time Count Down",
		key="time_count_down",
		entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
	),
    "inverter_rate_power": SolaXModbusSensorEntityDescription(
        name="Inverter Rated Power",
        key="inverter_rate_power",
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),
	"total_yield": SolaXModbusSensorEntityDescription(
		name="Total Yield",
		key="total_yield",
		native_unit_of_measurement=ENERGY_MEGA_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
        allowedtypes=ALLDEFAULT,
    ),


    # tranferred from GEN4_SENSOR_TYPES
    "selfuse_nightcharge_upper_soc": SolaXModbusSensorEntityDescription(
        name="Selfuse Night Charge Upper SOC",
        key="selfuse_nightcharge_upper_soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=DEVICE_CLASS_BATTERY,
        allowedtypes= GEN4,
    ),
    "selfuse_nightcharge_enable": SolaXModbusSensorEntityDescription(
        name="Selfuse Night Charge Enable",
        key="selfuse_nightcharge_enable",
        allowedtypes = GEN4,
    ),
    "charge_period2_enable": SolaXModbusSensorEntityDescription(
        name="Charge Period2 Enable",
        key="charge_period2_enable",
        entity_registry_enabled_default=False,
        allowedtypes = GEN4,
    ),
    "shadow_fix_enable": SolaXModbusSensorEntityDescription(
        name="Shadow Fix Function Level",
        key="shadow_fix_enable",
        entity_registry_enabled_default=False,
        allowedtypes = GEN4,
     ),
     "machine_type": SolaXModbusSensorEntityDescription(
        name="Machine Type X1/X3",
        key="machine_type",
        entity_registry_enabled_default=False,
        allowedtypes = GEN4,
     ),
     "manual_mode": SolaXModbusSensorEntityDescription(
        name="Manual Mode",
        key="manual_mode",
        allowedtypes = GEN4,
     ),
     "feedin_nightcharge_min_soc": SolaXModbusSensorEntityDescription(
        name="Feedin Night Charge Min SOC",
        key="feedin_nightcharge_min_soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=DEVICE_CLASS_BATTERY,
        allowedtypes = GEN4,
     ),
     "feedine_nightcharge_upper_soc": SolaXModbusSensorEntityDescription(
        name="Feedin Night Charge Upper SOC",
        key="feedin_nightcharge_upper_soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=DEVICE_CLASS_BATTERY,
        allowedtypes = GEN4,
     ),
     "backupnightcharge_min_soc": SolaXModbusSensorEntityDescription(
        name="Backup Night Charge Min SOC",
        key="backup_nightcharge_min_soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=DEVICE_CLASS_BATTERY,
        allowedtypes = GEN4,
     ),
     "backup_nightcharge_upper_soc": SolaXModbusSensorEntityDescription(
        name="Backup Night Charge Upper SOC",
        key="backup_nightcharge_upper_soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=DEVICE_CLASS_BATTERY,
        allowedtypes = GEN4,
     ),


     # transferred fromm GEN3_X1_SENSOR_TYPES, some also from GEN3_X3_SENSOR_TYPES

    "backup_charge_end": SolaXModbusSensorEntityDescription(
        name="Backup Charge End",
        key="backup_charge_end",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "backup_charge_start": SolaXModbusSensorEntityDescription(
        name="Backup Charge Start",
        key="backup_charge_start",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "backup_gridcharge": SolaXModbusSensorEntityDescription(
        name="Backup Gridcharge",
        key="backup_gridcharge",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "battery_input_energy_today": SolaXModbusSensorEntityDescription(
        name="Battery Input Energy Today",
        key="input_energy_charge_today",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        allowedtypes= X1 | X3 | GEN3 | GEN4,
    ),
    "battery_output_energy_today": SolaXModbusSensorEntityDescription(
        name="Battery Output Energy Today",
        key="output_energy_charge_today",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        allowedtypes= X1 | X3 | GEN3 | GEN4,
    ),
    "cloud_control": SolaXModbusSensorEntityDescription(
        name="Cloud Control",
        key="cloud_control",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3,
    ),
    "ct_meter_setting": SolaXModbusSensorEntityDescription(
        name="CT Meter Setting",
        key="ct_meter_setting",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | X3 | GEN3 | GEN4,
    ),
    "disch_cut_off_capacity_grid_mode": SolaXModbusSensorEntityDescription(
        name="Discharge Cut Off Capacity Grid Mode",
        key="disch_cut_off_capacity_grid_mode",
        native_unit_of_measurement=PERCENTAGE,
        allowedtypes= X1 | GEN3 | GEN4,
        entity_registry_enabled_default=False,
    ),
    "disch_cut_off_point_different": SolaXModbusSensorEntityDescription(
        name="Discharge Cut Off Point Different",
        key="disch_cut_off_point_different",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "disch_cut_off_voltage_grid_mode": SolaXModbusSensorEntityDescription(
        name="Discharge Cut Off Voltage Grid Mode",
        key="disch_cut_off_voltage_grid_mode",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "export_energy_today": SolaXModbusSensorEntityDescription(
        name="Today's Export Energy",
        key="export_energy_today",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        allowedtypes= X1 | X3 | GEN3 | GEN4,
    ),
    "forcetime_period_1_max_capacity": SolaXModbusSensorEntityDescription(
        name="Forcetime Period 1 Maximum Capacity",
        key="forcetime_period_1_max_capacity",
        native_unit_of_measurement=PERCENTAGE,
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "forcetime_period_2_max_capacity": SolaXModbusSensorEntityDescription(
        name="Forcetime Period 2 Maximum Capacity",
        key="forcetime_period_2_max_capacity",
        native_unit_of_measurement=PERCENTAGE,
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "global_mppt_function": SolaXModbusSensorEntityDescription(
        name="Global MPPT Function",
        key="global_mppt_function",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3,
    ),
    "import_energy_today": SolaXModbusSensorEntityDescription(
        name="Today's Import Energy",
        key="import_energy_today",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        allowedtypes= X1 | X3 | GEN3 | GEN4,
    ),
    "machine_style": SolaXModbusSensorEntityDescription(
        name="Machine Style",
        key="machine_style",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "meter_1_id": SolaXModbusSensorEntityDescription(
        name="Meter 1 id",
        key="meter_1_id",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "meter_2_id": SolaXModbusSensorEntityDescription(
        name="Meter 2 id",
        key="meter_2_id",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "meter_function": SolaXModbusSensorEntityDescription(
        name="Meter Function",
        key="meter_function",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "power_control_timeout": SolaXModbusSensorEntityDescription(
        name="Power Control Timeout",
        key="power_control_timeout",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3 | GEN4,
    ),
    "was4777_power_manager": SolaXModbusSensorEntityDescription(
        name="wAS4777 Power Manager",
        key="was4777_power_manager",
        entity_registry_enabled_default=False,
        allowedtypes= X1 | GEN3,
    ),


    # transferred fromm GEN3_X3_SENSOR_TYPES
     "earth_detect_x3": SolaXModbusSensorEntityDescription(
        name="Earth Detect X3",
        key="earth_detect_x3",
        allowedtypes = X3 | GEN3,
    ),
    "feedin_power_r": SolaXModbusSensorEntityDescription(
        name="Measured Power R",
        key="feedin_power_r",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "feedin_power_s": SolaXModbusSensorEntityDescription(
        name="Measured Power S",
        key="feedin_power_s",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "feedin_power_t": SolaXModbusSensorEntityDescription(
        name="Measured Power T",
        key="feedin_power_t",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "grid_current_r": SolaXModbusSensorEntityDescription(
        name="Inverter Current R",
        key="grid_current_r",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "grid_current_s": SolaXModbusSensorEntityDescription(
        name="Inverter Current S",
        key="grid_current_s",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "grid_current_t": SolaXModbusSensorEntityDescription(
        name="Inverter Current T",
        key="grid_current_t",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "grid_mode_runtime": SolaXModbusSensorEntityDescription(
        name="Grid Mode Runtime",
        key="grid_mode_runtime",
        native_unit_of_measurement=TIME_HOURS,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "grid_power_r": SolaXModbusSensorEntityDescription(
        name="Inverter Power R",
        key="grid_power_r",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "grid_power_s": SolaXModbusSensorEntityDescription(
        name="Inverter Power S",
        key="grid_power_s",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "grid_power_t": SolaXModbusSensorEntityDescription(
        name="Inverter Power T",
        key="grid_power_t",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "grid_service_x3": SolaXModbusSensorEntityDescription(
        name="Grid Service X3",
        key="grid_service_x3",
        allowedtypes = X3 | GEN3,
    ),
    "grid_voltage_r": SolaXModbusSensorEntityDescription(
        name="Inverter Voltage R",
        key="grid_voltage_r",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "grid_voltage_s": SolaXModbusSensorEntityDescription(
        name="Inverter Voltage S",
        key="grid_voltage_s",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "grid_voltage_t": SolaXModbusSensorEntityDescription(
        name="Inverter Voltage T",
        key="grid_voltage_t",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes = X3 | GEN3 | GEN4,
    ),
    "phase_power_balance_x3": SolaXModbusSensorEntityDescription(
        name="Phase Power Balance X3",
        key="phase_power_balance_x3",
        allowedtypes = X3 | GEN3 | GEN4,
    ),

    # transferred from X1_EPS_SENSOR_TYPES

    "eps_auto_restart": SolaXModbusSensorEntityDescription(
        name="EPS Auto Restart",
        key="eps_auto_restart",
        allowedtypes = X1 | X3 | GEN2 | GEN3,
    ),
    "eps_current": SolaXModbusSensorEntityDescription(
        name="EPS Current",
        key="eps_current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes = X1 | GEN2 | GEN3 | GEN4,
    ),
    "eps_frequency": SolaXModbusSensorEntityDescription(
        name="EPS Frequency",
        key="eps_frequency",
        native_unit_of_measurement=FREQUENCY_HERTZ,
        allowedtypes = X1 | X3  | GEN2 | GEN3 | GEN4,
    ),
    "eps_min_esc_soc": SolaXModbusSensorEntityDescription(
        name="EPS Min Esc SOC",
        key="eps_min_esc_soc",
        native_unit_of_measurement=PERCENTAGE,
        allowedtypes = X1 | X3 | GEN2 | GEN3,
    ),
    "eps_min_esc_voltage": SolaXModbusSensorEntityDescription(
        name="EPS Min Esc Voltage",
        key="eps_min_esc_voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        allowedtypes = X1 | X3 | GEN2 | GEN3,
    ),
    "eps_mute": SolaXModbusSensorEntityDescription(
        name="EPS Mute",
        key="eps_mute",
        allowedtypes = X1 | X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_power": SolaXModbusSensorEntityDescription(
        name="EPS Power",
        key="eps_power",
        native_unit_of_measurement=POWER_VOLT_AMPERE,
        allowedtypes = X1 | GEN2 | GEN3 | GEN4,
    ),
    "eps_set_frequency": SolaXModbusSensorEntityDescription(
        name="EPS Set Frequency",
        key="eps_set_frequency",
        native_unit_of_measurement=FREQUENCY_HERTZ,
        allowedtypes = X1 | X3 | GEN2 | GEN3,
    ),
    "eps_voltage": SolaXModbusSensorEntityDescription(
        name="EPS Voltage",
        key="eps_voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes = X1 | GEN2 | GEN3 | GEN4,
    ),
    "eps_yield_today": SolaXModbusSensorEntityDescription(
        name="EPS Yield Today",
        key="eps_yield_today",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        #state_class=STATE_CLASS_TOTAL_INCREASING,
        allowedtypes = X1 | X3 | GEN2 | GEN3 | GEN4,
    ),

    # transferred from X3_EPS_SENSOR_TYPES

    "eps_current_r": SolaXModbusSensorEntityDescription(
        name="EPS Current R",
        key="eps_current_r",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
        ),
    "eps_current_s": SolaXModbusSensorEntityDescription(
        name="EPS Current S",
        key="eps_current_s",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_current_t": SolaXModbusSensorEntityDescription(
        name="EPS Current T",
        key="eps_current_t",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_mode_runtime": SolaXModbusSensorEntityDescription(
        name="EPS Mode Runtime",
        key="eps_mode_runtime",
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_power_r": SolaXModbusSensorEntityDescription(
        name="EPS Power R",
        key="eps_power_r",
        native_unit_of_measurement=POWER_VOLT_AMPERE,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_power_s": SolaXModbusSensorEntityDescription(
        name="EPS Power S",
        key="eps_power_s",
        native_unit_of_measurement=POWER_VOLT_AMPERE,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_power_t": SolaXModbusSensorEntityDescription(
        name="EPS Power T",
        key="eps_power_t",
        native_unit_of_measurement=POWER_VOLT_AMPERE,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_power_active_r": SolaXModbusSensorEntityDescription(
        name="EPS Power Active R",
        key="eps_power_active_r",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_power_active_s": SolaXModbusSensorEntityDescription(
        name="EPS Power Active S",
        key="eps_power_active_s",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_power_active_t": SolaXModbusSensorEntityDescription(
        name="EPS Power Active T",
        key="eps_power_active_t",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_voltage_r": SolaXModbusSensorEntityDescription(
        name="EPS Voltage R",
        key="eps_voltage_r",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_voltage_s": SolaXModbusSensorEntityDescription(
        name="EPS Voltage S",
        key="eps_voltage_s",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),
    "eps_voltage_t": SolaXModbusSensorEntityDescription(
        name="EPS Voltage T",
        key="eps_voltage_t",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        allowedtypes = X3 | GEN2 | GEN3 | GEN4,
    ),

}

