import lgpio

import lgpio

_h = lgpio.gpiochip_open(0)
_setup_pins = set()

OUT = 0
IN = 1
LOW = 0
HIGH = 1

def setup(pin, mode):
    if pin not in _setup_pins:
        lgpio.gpio_claim_output(_h, pin)
        _setup_pins.add(pin)

def output(pin, value):
    if pin not in _setup_pins:
        lgpio.gpio_claim_output(_h, pin)
        _setup_pins.add(pin)
    lgpio.gpio_write(_h, pin, value)

def input(pin):
    return lgpio.gpio_read(_h, pin)

def cleanup():
    lgpio.gpiochip_close(_h)
