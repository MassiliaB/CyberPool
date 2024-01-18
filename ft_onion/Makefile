build:
	docker build -t tor .

run:
	docker run -d --name tor -p 80:80 tor

run_:
	docker run -it -p 80:80 tor

exec:
	docker exec -it tor_container

clear_and_run: clear build run_

clear:
	@docker ps -q | xargs docker stop
	@docker ps -aq | xargs docker rm

clear_all:
	docker system prune