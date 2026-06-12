# mic-icon Makefile

PREFIX ?= $(HOME)/.local

install:
	mkdir -p $(PREFIX)/bin
	install -Dm755 mic-icon $(PREFIX)/bin/mic-icon

remove:
	rm -f $(PREFIX)/bin/mic-icon

.PHONY: install remove
