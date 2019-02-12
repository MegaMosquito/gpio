all: build run

build:
	docker build -t gpio_server .

dev: build stop
	-docker rm -f gpio_server 2> /dev/null || :
	docker run -it --privileged --name gpio_server --net=host -p 6667:6667 --volume `pwd`:/outside gpio_server /bin/sh

run: stop
	-docker rm -f speedtest 2>/dev/null || :
	docker run -d --privileged --name gpio_server --net=host --volume `pwd`:/outside gpio_server

exec:
	docker exec -it gpio_server /bin/sh

stop:
	-docker rm -f gpio_server 2>/dev/null || :

clean: stop
	-docker rmi gpio_server 2>/dev/null || :

.PHONY: all build dev run exec stop clean
