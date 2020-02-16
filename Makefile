all: build run

build:
	docker build -t ibmosquito/gpio_server:1.0.0 .

dev: build stop
	-docker rm -f gpio_server 2> /dev/null || :
	docker run -it --privileged --name gpio_server -p 6667:6667 --volume `pwd`:/outside ibmosquito/gpio_server:1.0.0 /bin/sh

run: stop
	-docker rm -f speedtest 2>/dev/null || :
	docker run -d --privileged --name gpio_server -p 6667:6667 ibmosquito/gpio_server:1.0.0

test:
	curl -X POST -sS localhost:6667/gpio/v1/mode/bcm
	curl -X POST -sS localhost:6667/gpio/v1/configure/14/out
	curl -X POST -sS localhost:6667/gpio/v1/configure/15/out
	curl -X POST -sS localhost:6667/gpio/v1/14/0
	curl -X POST -sS localhost:6667/gpio/v1/15/0

exec:
	docker exec -it gpio_server /bin/sh

push:
	docker push ibmosquito/gpio_server:1.0.0

stop:
	-docker rm -f gpio_server 2>/dev/null || :

clean: stop
	-docker rmi ibmosquito/gpio_server:1.0.0 2>/dev/null || :

.PHONY: all build dev run test exec stop clean
