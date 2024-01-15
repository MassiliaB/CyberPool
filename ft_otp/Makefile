.PHONY: run

PYTHON = python3
SCRIPT = ft_otp

all:
	run
	ifeq ($(ARG),)
	$(error Usage: make ARG=<key_file>)
	endif

run:
	@cat $(ARG) | xxd -p -c 1000000 > key.hex
	@len=$$(wc -c < key.hex); \
	if [ $$len -lt 64 ]; then \
		echo "Warning ! key.hex has less than 64 characters"; \
		exit 1; \
	fi
	else
		echo "key.hex succesfully created !"; \
	fi

clear:
	@rm *.key *.hex *.txt
	echo "All clear !"; 