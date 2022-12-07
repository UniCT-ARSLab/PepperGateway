# Makefile for testing purposes (i.e. gateway). It is a copy of the main Makefile, but in a different folder.
build:
	docker build -t pepper-testing .  

run-test:
	docker run --rm -it -p 5000:5000 -v /Users/giuseppepitruzzella/PepperGateway/gateway/:/app/ --name gw pepper-testing

run:
	docker run --rm -it -p 6566:6566 -p 5000:5000 -v /Users/giuseppepitruzzella/PepperGateway/gateway/:/app/ --name gw pepper-testing

run-flask:
	docker run --rm -it -p 5000:5000 --name gw pepper-testing