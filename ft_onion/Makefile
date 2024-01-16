build:
	docker build -t tor .

run:
	docker run -d --name tor_container -p 8080:80 tor

exec:
	docker exec -it tor_container /bin/sh

clear:
	docker stop tor_container && docker rm tor_container