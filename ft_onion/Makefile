build:
	docker build -t tor .

run:
	docker run -d --name tor tor -v

run_:
	docker run -it tor /bin/bash

exec:
	docker exec -it tor /bin/bash

clear_and_run: clear build run_

clear:
	@docker ps -q | xargs docker stop
	@docker ps -aq | xargs docker rm

clear_all:
	docker system prune