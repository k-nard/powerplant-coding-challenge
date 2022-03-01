# QUICK HOW TO

## Container Way

### build container image
`$ podman/docker build -t $(basename $(realpath .)):latest .`

### run container
`$ podman/docker run -ti --rm --name $(basename $(realpath .)) -p 8888:8888 $(basename $(realpath .)):latest`

### test the rest api
`$ curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload3.json http://localhost:8888/productionplan`

## 

### Launch REST API

`$ python3 manage.py runserver 127.0.0.1:8888  # 0.0.0.0:8888 if REST request from external`

### test the rest api
`$ curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload3.json http://localhost:8888/productionplan`
