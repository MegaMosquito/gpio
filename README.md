# gpio

This container exposes Raspberry Pi GPIO pins through a REST API on port 6667. Before you can use a pin, you must first "configure" the pin for "in"-put or "out"-put. If configuring the pin for input, you may optionally configure a pull-"up" or pull-"down" resistor (and if none is specified a pullup resistor is configured). The pin numbering is *board* numbering. That is, you cannot use the Broadcom chip GPIO number, but instead you must use the sequential pin numbers as they appear on the board connector. That is, the numbers shown in the circles within the connector image on the diagram on this page:

 *  https://www.raspberrypi.org/documentation/usage/gpio/
    
You could modify a single line in the source to change to using the Broadcom chip pin numbers if you prefer (this is documented near the top of the source file), here:

 *  https://github.com/MegaMosquito/gpio/blob/master/gpio_server.py#L22

After configuring the pin appropriately, you can use either the "get" or "set" APIs. Note that these are digital GPIO pins so they will either be "true" or "false". The "set" API accepts those values, or it will accept "0" or "1" (representing "false" or "true", respectively).

## API details in brief...

### CONFIGURE:

`POST "/gpio/v1/configure/<pin>/<inout>/<pull>"`, or
`POST "/gpio/v1/configure/<pin>/<inout>"`:
 - where `<pin>` is a board pin number, in {1 .. 40},
 - and `<inout>` is either "in" or "out",
 - and `<pull>` is either "up" or "down".

### GET:

`GET "/gpio/v1/get/<pin>"`:
 - where `<pin>` is a board pin number, in {1 .. 40}.

### SET:

`POST "/gpio/v1/set/<pin>/<state>"`:
 - where `<pin>` is a board pin number, in {1 .. 40},
 - and `<state>` is either "false" (or "0") or "true" (or "1").




