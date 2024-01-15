.PHONY: generate

PYTHON = python3
SCRIPT = ft_otp

ifeq ($(ARG),)
$(error Usage: make ARG=<key_file>)
endif

generate:
	@cat $(ARG) | xxd -p -c 1000000 > key.hex
	@len=$$(wc -c < key.hex); \
	if [ $$len -lt 64 ]; then \
		echo "Warning ! ft_otp.key has less than 64 characters"; \
		exit 1; \
	fi