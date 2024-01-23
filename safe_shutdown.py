#!/usr/bin/env python
# -*- coding: utf-8 -*-
# safe_shutdown_Pi.py
#
# -----------------------------------------------------------------------------
#                 Raspberry Pi Safe Shutdown Python Script
# -----------------------------------------------------------------------------
# Based on code from the Sparkfun electronics:
# WRITTEN BY: Ho Yun "Bobby" Chan
# @ SparkFun Electronics
# DATE: 3/31/2020
#
# ==================== DESCRIPTION ====================
# built-in general purpose button to safely reboot/shutdown you Pi:
#    1.) If you press the button momentarily, the Pi will shutdown.
#
# ========== TUTORIAL ==========
#  For more information on running this script on startup,
#  check out the associated tutorial to adjust your "rc.local" file:
#  https://learn.sparkfun.com/tutorials/raspberry-pi-safe-reboot-and-shutdown-button
#
import time
import RPi.GPIO as GPIO
# Pin definition
shutdown_pin = 18
# Suppress warnings
GPIO.setwarnings(False)
# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)
# Use built-in internal pullup resistor so the pin is not floating
# if using a momentary push button without a resistor.
GPIO.setup(shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# modular function to shutdown Pi
def shut_down():
    print("shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

# Check button if we want to shutdown the Pi safely
while True:
    #short delay, otherwise this code will take up a lot of the Pi's processing power
    time.sleep(0.5)

    # For troubleshooting, uncomment this line to output buton status on command line
    #print('GPIO state is = ', GPIO.input(shutdown_pin))
    if GPIO.input(shutdown_pin)== False:
        shut_down()
