## QUICK HOW TO

### build container image
`$ podman build -t $(basename $(realpath .)):latest .`

### run container
`$ podman run -ti --rm --name $(basename $(realpath .)) -p 8888:8888 $(basename $(realpath .)):latest`

### test the rest api
`$ curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload3.json http://localhost:8888/productionplan`
