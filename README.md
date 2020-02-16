# gpio

This container exposes Raspberry Pi GPIO pins through a REST API on port 6667.

Before you can do anything else with this service, you must use the "mode" API to tell it whether you wish to use Broadcom pin numbering (i.e., the numbering of the pins on the Broadcom SOC) or "board" pin numbering (i.e., the sequential pin numbers as they appear on the board connector). The board pin numbers are shown in the circles within the connector image on the diagram on this page, while the Boradcom pin numbers are shown on either side of the connector image, with "GPIO" prefixes:

 *  https://www.raspberrypi.org/documentation/usage/gpio/

After you have set the mode, you must use the "configure" API to configure the pins you wish to use (i.e., configure them for input or output use). If you are configuring for input, specify a pull-up or pull-down resistor (if none is specified a pullup resistor is automatically configured).

Once all of that preparation is complete, you can use either the "GET" or "POST" pin number APIs shown below. Note that GPIO pins are treated as purely digital so they will either show "true" or "false". The "POST" API accepts those literal values, but it will also accept "0" or "1" (representing "false" or "true", respectively).

## Usage:

```
make build
make run
make test
```

## API details in brief...

### MODE:

You must set the mode before doing anything else with this service.

`POST "/gpio/v1/mode/<bcm-or-board>"`:
 - where `<bcm-or-board>` is either "bcm" or "board".

### CONFIGURE:

You must configure a GPIO pin for input or output before using its GET or POST.

`POST "/gpio/v1/configure/<pin>/<inout>/<pull>"`, or
`POST "/gpio/v1/configure/<pin>/<inout>"`:
 - where `<pin>` is a board pin number, in {1 .. 40},
 - and `<inout>` is either "in" or "out",
 - and `<pull>` is either "up" or "down".

### GET:

Get the current value of a GPIO pin that was previously configured for input.

`GET "/gpio/v1/<pin>"`:
 - where `<pin>` is a board pin number, in {1 .. 40}.

### POST:

Set the value of a GPIO pin that was previously configured for output.

`POST "/gpio/v1/<pin>/<state>"`:
 - where `<pin>` is a board pin number, in {1 .. 40},
 - and `<state>` is either "false" (or "0") or "true" (or "1").


