#
# REST API for access to selected GPIO pins
#
# Written by Glen Darling, February 2019.
#

from flask import Flask
import json
import subprocess
import threading
import time

# Import the GPIO library so python can work with the GPIO pins
import RPi.GPIO as GPIO

# REST API details
REST_API_BIND_ADDRESS = '0.0.0.0'
REST_API_PORT = 6667
webapp = Flask('gpio')

# Setup the GPIO module
GPIO.setwarnings(True)

# A global to indicate the mode
mode = None

# Non-GPIO "board" pins
non_gpio = [1, 2, 4, 6, 9, 14, 17, 20, 25, 30, 34, 39]


# Validate the pin number string (using BOARD numbering)
def valid_pin(pinstr):
  global mode
  pin_min = 1
  pin_max = 40
  if "bcm" == mode:
    pin_max = 26
  try:
    pin = int(pinstr)
    if pin < pin_min or pin > pin_max:
      return False
    return True
  except:
    return False


# The web server code


# MODE: <board|bcm>
@webapp.route("/gpio/v1/mode/<bcmorboard>", methods=['POST'])
def gpio_mode(bcmorboard):
  global mode
  bcmorboard = bcmorboard.lower()
  if None != mode:
    return ('{"error": "Mode is already set to %s."}' % mode)
  elif "bcm" == bcmorboard:
    GPIO.setmode(GPIO.BCM)
    mode = "bcm"
    return ('{"mode": "bcm"}\n')
  elif "board" == bcmorboard:
    GPIO.setmode(GPIO.BOARD)
    mode = "board"
    return ('{"mode": "board"}\n')
  else:
    return ('{"error": "Unrecognized mode, %s."}' % bcmorboard)


# CONFIGURE: <number>/<in|out>/<up|down>
@webapp.route("/gpio/v1/configure/<pin>/<inout>", methods=['POST'])
@webapp.route("/gpio/v1/configure/<pin>/<inout>/<pull>", methods=['POST'])
def gpio_config(pin, inout, pull=None):
  if None == mode:
    return ('{"error": "Mode is not set."}\n')
  elif not valid_pin(pin):
    return ('{"error": "Unrecognized pin number: %s."}\n' % pin)
  elif "board" == mode and pin in non_gpio:
    return ('{"error": "Board pin number %s is not a GPIO pin."}\n' % pin)
  elif "in" != inout and "out" != inout:
    return ('{"error": "Unrecognized direction: %s"}\n' % inout)
  elif None != pull and not ("up" == pull or "down" == pull):
    return ('{"error": "Unrecognized pull value: %s"}\n' % pull)
  elif "out" == inout and None != pull:
    return ('{"error": "Direction is out but pull %s specified."}\n' % pull)
  else:
    pin = int(pin)
    if "in" == inout and (None == pull or "up" == pull):
      print("Configuring pin %d for INPUT (with a pull-up resistor)." % pin)
      GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      return ('{"configured": %d, "direction": "in", "pull": "up"}\n' % pin)
    elif "in" == inout and "down" == pull:
      print("Configuring pin %d for INPUT (with a pull-down resistor)." % pin)
      GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
      return ('{"configured": %d, "direction": "in", "pull": "down"}\n' % pin)
    elif "out" == inout:
      print("Configuring pin %d for OUTPUT." % pin)
      GPIO.setup(pin, GPIO.OUT)
      return ('{"configured": %d, "direction": "out"}\n' % pin)
  return ('{"error": "UNREACHABLE!"}')


# GET: <number>
@webapp.route("/gpio/v1/<pin>", methods=['GET'])
def gpio_get(pin):
  if None == mode:
    return ('{"error": "Mode is not set."}\n')
  elif not valid_pin(pin):
    return ('{"error": "Unrecognized pin number: %s."}\n' % pin)
  else:
    pin = int(pin)
    if GPIO.input(pin) == GPIO.LOW:
      return ('{"pin": %d, "state": false}\n' % pin)
    elif GPIO.input(pin) == GPIO.HIGH:
      return ('{"pin": %d, "state": true}\n' % pin)
    return ('{"error": "Undefined value returned for pin %d."}\n' % pin)


# POST: <number>/<0|1> or <number>/<true|false>
@webapp.route("/gpio/v1/<pin>/<state>", methods=['POST'])
def gpio_post(pin, state):
  if None == mode:
    return ('{"error": "Mode is not set."}\n')
  elif not valid_pin(pin):
    return ('{"error": "Unrecognized pin number: %s."}\n' % pin)
  elif "0" != state and "1" != state and "false" != state and "true" != state:
    return ('{"error": "Unrecognized state value: %s}\n' % state)
  else:
    pin = int(pin)
    if "0" == state or "false" == state:
      GPIO.output(pin, GPIO.LOW)
      return ('{"pin": %d, "state": false}\n' % pin)
    else:
      GPIO.output(pin, GPIO.HIGH)
      return ('{"pin": %d, "state": true}\n' % pin)


# Main program (to start the web server thread)
if __name__ == '__main__':
  webapp.run(host=REST_API_BIND_ADDRESS, port=REST_API_PORT)

