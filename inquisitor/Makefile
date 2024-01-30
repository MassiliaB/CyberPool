all: build

print_error:
ifeq ($(strip $(ARGS)$(SCAN)),)
	@echo "Error: Please provide the required arguments or options."
	@echo "Usage:"
	@echo "  make run ARGS=\"ip_src mac_src ip_target mac_target\""
	@echo "  make run_scan SCAN=\"option ip\""
	@exit 1
endif

build:
	@echo "Building victim's container"
	docker build -t victim -f victim/Dockerfile .
	@echo "Building attacker's container"
	docker build -t attacker -f attacker/Dockerfile .

inspect:
	docker network inspect inquisitor_network

up:
	docker-compose up

run:
	@echo "Runnin victim's container"
	docker run -d --name victim victim --network network
	@echo "Runnin attacker's container"
	docker run -d --name attacker attacker --network network

vexec:
	docker exec -it victim /bin/bash

aexec:
	docker exec -it attacker /bin/bash

clear_and_run: clear build up

stop:
	@CONTAINERS=$$(docker ps -q); \
	if [ -n "$$CONTAINERS" ]; then \
	docker stop $$CONTAINERS; \
	else \
	echo "No running containers to stop."; \
	fi
	docker-compose down

rm:
	@CONTAINERS=$$(docker ps -a -q); \
	if [ -n "$$CONTAINERS" ]; then \
	docker rm $$CONTAINERS; \
	else \
	echo "No containers to remove."; \
	fi

clear_network:
	docker network prune

clear: stop rm clean_network

clear_all: clear_network
	docker system prune

.PHONY: run run_scan clear_and_run clear clear_all