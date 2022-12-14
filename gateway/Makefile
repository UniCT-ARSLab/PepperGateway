# Makefile for testing purposes (i.e. Gateway). It is a copy of the main Makefile, but in a different folder.
build:
	docker build -t pepper-testing .  

run-test:
	docker run --rm -it -p 5000:5000 -v /Users/giuseppepitruzzella/PepperGateway/Gateway/:/app/ --name gw pepper-testing

run:
	docker run --rm -it -p 6566:6566 -p 5000:5000 -v /Users/giuseppepitruzzella/PepperGateway/Gateway/:/app/ --name gw pepper-testing

run-flask:
	docker run --rm -it -p 5000:5000 --name gw pepper-testing