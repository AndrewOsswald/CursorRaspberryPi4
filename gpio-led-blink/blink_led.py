#!/usr/bin/env python3
"""
Blink an LED on GPIO 17 (BCM) at 1 Hz.
Wiring: LED anode → 330 Ω resistor → GPIO 17 (physical pin 11). LED cathode → GND.
Run: python3 gpio-led-blink/blink_led.py  (stop with Ctrl+C)
"""
from gpiozero import LED
from signal import pause

LED_GPIO = 17  # BCM; physical pin 11

def main() -> None:
    led = LED(LED_GPIO)
    try:
        led.blink(on_time=0.5, off_time=0.5)  # 1 Hz
        pause()
    finally:
        led.close()

if __name__ == "__main__":
    main()
