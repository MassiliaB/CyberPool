ARGS ?= ip_src max_src ip_target mac_target
SCAN ?= option ip

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
	docker build -t spoof .

run: print_error
	docker run -d --name spoof spoof $(ARGS)

run_scan: print_error
	docker run -d --name spoof spoof $(SCAN)

exec:
	docker exec -it spoof /bin/bash

clear_and_run: clear build run

clear:
	@docker ps -q | xargs docker stop
	@docker ps -aq | xargs docker rm

clear_all:
	docker system prune

.PHONY: run run_scan clear_and_run clear clear_all