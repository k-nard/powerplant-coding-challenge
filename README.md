# QUICK HOW TO

## Container Way

### build container image
`$ podman/docker build -t powerplant-coding-challenge:latest .`

### run container
`$ podman/docker run -ti --rm --name powerplant-coding-challenge -p 8888:8888 powerplant-coding-challenge:latest`

### test the rest api
`$ curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload3.json http://localhost:8888/productionplan`

## Simple Python/Django way

### Launch REST API

`$ python3 manage.py runserver 127.0.0.1:8888`

### test the rest api
`$ curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload3.json http://localhost:8888/productionplan`
