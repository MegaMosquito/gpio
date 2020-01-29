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
GPIO.setmode(GPIO.BOARD) # or GPIO.BCM (Note: must change valid_pin() to match!)
GPIO.setwarnings(True)

# Validate the pin number string (using BOARD numbering)
def valid_pin(pinstr):
  try:
    pin = int(pinstr)
    if pin < 0 or pin > 40:
      return False
    return True
  except:
    return False

# The web server code


# CONFIGURE: <number>/<in|out>/<up|down>
@webapp.route("/gpio/v1/configure/<pin>/<inout>", methods=['POST'])
@webapp.route("/gpio/v1/configure/<pin>/<inout>/<pull>", methods=['POST'])
def gpio_config(pin, inout, pull=None):
  if not valid_pin(pin):
    return ('{"error": "Unrecognized pin number: %s."}\n' % pin)
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
@webapp.route("/gpio/v1/get/<pin>", methods=['GET'])
def gpio_get(pin):
  if not valid_pin(pin):
    return ('{"error": "Unrecognized pin number: %s."}\n' % pin)
  else:
    pin = int(pin)
    if GPIO.input(pin) == GPIO.LOW:
      return ('{"pin": %d, "state": false}\n' % pin)
    elif GPIO.input(pin) == GPIO.HIGH:
      return ('{"pin": %d, "state": true}\n' % pin)
    return ('{"error": "Undefined value returned for pin %d."}\n' % pin)


# SET: <number>/<0|1> or <number>/<true|false>
@webapp.route("/gpio/v1/set/<pin>/<state>", methods=['POST'])
def gpio_set(pin, state):
  if not valid_pin(pin):
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

