build:
	docker build -t hiro:latest -f ./docker/Dockerfile .

run:
	docker run --rm -v $$PWD/src/:/app/ -p 12001:8080 hiro:latest
