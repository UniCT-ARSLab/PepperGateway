build:
	docker build -t pepper-gateway .

run:
	docker run --rm -it -p 6566:6566 -v /Users/giuseppepitruzzella/pepper_robot:/app/ --name gw pepper-gateway