"""
Pin configuration for two Wio-SX1262 modules on Raspberry Pi 4 (BCM numbering).

Source: sx1262_gpio_test/context/wiring.md and agent/system-environment.md.
"""

# Module A (CE0 / spidev0.0)
MODULE_A = {
    "nrst": 17,   # Physical 11
    "busy": 18,   # Physical 12
    "dio1": 22,   # Physical 15
    "rf_sw": 23,  # Physical 16
}

# Module B (CE1 / spidev0.1)
MODULE_B = {
    "nrst": 25,   # Physical 22
    "busy": 5,    # Physical 29
    "dio1": 6,    # Physical 31
    "rf_sw": 12,  # Physical 32
}
