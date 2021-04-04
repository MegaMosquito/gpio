# gpio

This container exposes Raspberry Pi GPIO pins through a REST API on port 6667.

Before you can do anything else with this service, you must use the "mode" API to tell it whether you wish to use Broadcom ("bcm")pin numbering (i.e., the numbering of the pins on the Broadcom SOC) or "board" pin numbering (i.e., the sequential pin numbers as they appear on the board connector). The board pin numbers are shown in parentheses, i.e., "()", in the table below, while the Broadcom pin numbers are shown on either side of them with "GPIO" prefixes:

```
   3V3  (1) (2)  5V    
 GPIO2  (3) (4)  5V    
 GPIO3  (5) (6)  GND   
 GPIO4  (7) (8)  GPIO14
   GND  (9) (10) GPIO15
GPIO17 (11) (12) GPIO18
GPIO27 (13) (14) GND   
GPIO22 (15) (16) GPIO23
   3V3 (17) (18) GPIO24
GPIO10 (19) (20) GND   
 GPIO9 (21) (22) GPIO25
GPIO11 (23) (24) GPIO8 
   GND (25) (26) GPIO7 
 GPIO0 (27) (28) GPIO1 
 GPIO5 (29) (30) GND   
 GPIO6 (31) (32) GPIO12
GPIO13 (33) (34) GND   
GPIO19 (35) (36) GPIO16
GPIO26 (37) (38) GPIO20
   GND (39) (40) GPIO21
```

For example, as you can see above, Broadcom GPIO #2 is located at board pin #3. 

Board pins may be numbered from 1 through 40, but many of those numbers are not valid GPIOs (e.g., board pin #1 is "3V3", a power pin, not a GPIO). Broadcom GPIO numbers range from 1 through 26 and all are valid GPIOs. When you use the "configure" and GET/POST pin APIs, they will check to see if you are passing a valid GPIO or board pin number and return an error if you are not.

After you have set the mode, you must use the "configure" API to configure the pins you wish to use (i.e., configure them for input or output use). If you are configuring for input, specify a pull-up or pull-down resistor (if none is specified a pullup resistor is automatically configured).

Once all of that preparation is complete, you can use either the "GET" or "POST" pin number APIs shown below. Note that GPIO pins are treated as purely digital so they will either show "true" or "false". The "POST" API accepts those literal values, but it will also accept "0" or "1" (representing "false" or "true", respectively).

## Usage:

```
make build
make run
```

After doing that, you should be able to use the REST APIs described below. A quick test can be done with this command:

```
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
 - where `<pin>` is a chip or board pin number, as explained above,
 - and `<inout>` is either "in" or "out",
 - and `<pull>` is either "up" or "down".

### GET:

Get the current value of a GPIO pin that was previously configured for input.

`GET "/gpio/v1/<pin>"`:
 - where `<pin>` is a chip or board pin number, as explained above.

### POST:

Set the value of a GPIO pin that was previously configured for output.

`POST "/gpio/v1/<pin>/<state>"`:
 - where `<pin>` is a chip or board pin number, as explained above,
 - and `<state>` is either "false" (or "0") or "true" (or "1").


