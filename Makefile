build-main:
	docker build -t pepper-gateway .

run-main:
	docker run --rm -it -p 6566:6566 -v /Users/giuseppepitruzzella/PepperGateway:/app/ --name gw pepper-gateway

build-env:
	docker build -t pepper-env -f pepper-env .  

run-env:
	docker run --rm -it -p 6566:6566 -v /Users/giuseppepitruzzella/PepperGateway/:/app/ --name gw pepper-env