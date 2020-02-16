all: build run

build:
	docker build -t gpio_server .

dev: build stop
	-docker rm -f gpio_server 2> /dev/null || :
	docker run -it --privileged --name gpio_server -p 6667:6667 --volume `pwd`:/outside gpio_server /bin/sh

run: stop
	-docker rm -f speedtest 2>/dev/null || :
	docker run -d --privileged --name gpio_server -p 6667:6667 gpio_server

test:
	curl -X POST -sS localhost:6667/gpio/v1/mode/bcm
	curl -X POST -sS localhost:6667/gpio/v1/configure/14/out
	curl -X POST -sS localhost:6667/gpio/v1/configure/15/out
	curl -X POST -sS localhost:6667/gpio/v1/14/0
	curl -X POST -sS localhost:6667/gpio/v1/15/0

exec:
	docker exec -it gpio_server /bin/sh

stop:
	-docker rm -f gpio_server 2>/dev/null || :

clean: stop
	-docker rmi gpio_server 2>/dev/null || :

.PHONY: all build dev run exec stop clean
