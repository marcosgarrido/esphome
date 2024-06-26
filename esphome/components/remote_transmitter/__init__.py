import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import remote_base, esp32_rmt
from esphome.const import CONF_CARRIER_DUTY_PERCENT, CONF_ID, CONF_PIN, CONF_RMT_CHANNEL

AUTO_LOAD = ["remote_base"]
remote_transmitter_ns = cg.esphome_ns.namespace("remote_transmitter")
RemoteTransmitterComponent = remote_transmitter_ns.class_(
    "RemoteTransmitterComponent", remote_base.RemoteTransmitterBase, cg.Component
)

MULTI_CONF = True
CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(RemoteTransmitterComponent),
        cv.Required(CONF_PIN): pins.gpio_output_pin_schema,
        cv.Required(CONF_CARRIER_DUTY_PERCENT): cv.All(
            cv.percentage_int, cv.Range(min=1, max=100)
        ),
        cv.Optional(CONF_RMT_CHANNEL): esp32_rmt.validate_rmt_channel(tx=True),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    pin = await cg.gpio_pin_expression(config[CONF_PIN])
    if (rmt_channel := config.get(CONF_RMT_CHANNEL, None)) is not None:
        var = cg.new_Pvariable(config[CONF_ID], pin, rmt_channel)
    else:
        var = cg.new_Pvariable(config[CONF_ID], pin)
    await cg.register_component(var, config)

    cg.add(var.set_carrier_duty_percent(config[CONF_CARRIER_DUTY_PERCENT]))
