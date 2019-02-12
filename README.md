# gpio

A container that makes selected Raspberry Pi GPIO pins available through a REST API on port 6667. The pins are hard-coded with names at this point and you can use the following URI forms:

 * `GET "/v1/get_gpio/<name>`
 * `POST "/v1/set_gpio/<name>/<true-or-false>`

