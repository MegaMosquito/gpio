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

# How long to pause between runs of the test (in seconds)
#SECONDS_BETWEEN_TESTS = 20
SECONDS_BETWEEN_TESTS = (60 * 15)

# REST API details
REST_API_BIND_ADDRESS = '0.0.0.0'
REST_API_PORT = 6667
webapp = Flask('gpio')

# Setup the GPIO module
GPIO.setmode(GPIO.BCM) # or GPIO.BOARD
GPIO.setwarnings(True)

# Configure the output pins being used 
LEFT_OUTPUT_PIN = 14   # The one closer to the center, yellow wire
RIGHT_OUTPUT_PIN = 15  # The one closer to the outside edge, blue wire
GPIO.setup(LEFT_OUTPUT_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RIGHT_OUTPUT_PIN, GPIO.OUT, initial=GPIO.HIGH)

# Mapping of names-to-output-pins
output_pin_map = {
  "left": LEFT_OUTPUT_PIN,
  "right": RIGHT_OUTPUT_PIN,
}

# Configure the input pins being used
LEFT_INPUT_PIN = 16    # Left ESP01, red wire, SSID "The Shire"
MIDDLE_INPUT_PIN = 20  # Middle ESP01, orange wire, no module connected
RIGHT_INPUT_PIN = 21   # Right ESP01, yellow wire, SSID "Hobbiton"
GPIO.setup(LEFT_INPUT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(MIDDLE_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RIGHT_INPUT_PIN,  GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Mapping of names-to-input-pins
input_pin_map = {
  "The Shire": LEFT_INPUT_PIN,
  "Hobbiton": RIGHT_INPUT_PIN,
}

# GPIO.add_event_detect(PIN, GPIO.FALLING, bouncetime=200) # or GPIO.RISING
# if GPIO.event_detected(PIN): ...
# while GPIO.input(PIN) == GPIO.LOW: ...
# GPIO.output(PIN, GPIO.LOW) # GPIO.HIGH

# The web server code

# GET
@webapp.route("/v1/get_gpio/<name>", methods=['GET'])
def get_gpio(name):
  if not (name in input_pin_map):
    return ('{"error": "Unrecognized pin name: %s."}\n' % (name))
  else:
    pin = input_pin_map[name]
    if GPIO.input(pin) == GPIO.HIGH: return ('{"%s": true}\n' % (name))
    if GPIO.input(pin) == GPIO.LOW: return ('{"%s": false}\n' % (name))
    return ('{"error": "Undefined value found for pin name %s."}\n' % (name))

# POST
@webapp.route("/v1/set_gpio/<name>/<state>", methods=['POST'])
def set_gpio(name, state):
  if not (name in output_pin_map):
    return ('{"error": "Unrecognized pin name: %s."}\n' % (name))
  else:
    pin = output_pin_map[name]
    if "true" == state:
      GPIO.output(pin, GPIO.HIGH)
    elif "false" == state:
      GPIO.output(pin, GPIO.LOW)
    else:
      return ('{"error": "Bad value %s requested for pin name %s."}\n' % (state, name))
    return ('{"%s": "%s"}\n' % (name, state))

# Main program (to instantiate and start the 3 threads)
if __name__ == '__main__':
  webapp.run(host=REST_API_BIND_ADDRESS, port=REST_API_PORT)

