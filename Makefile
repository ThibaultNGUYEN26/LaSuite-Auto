SHELL := bash
export PATH := $(HOME)/.local/bin:$(PATH)

.DEFAULT_GOAL := help

.PHONY: help setup env back-install front-install back backend front frontend dev build check-uv

help:
	@printf '%s\n' \
		'make setup          Install backend and frontend dependencies' \
		'make back           Start the orchestrator backend' \
		'make front          Start the Electron frontend' \
		'make dev            Start backend and frontend together' \
		'make build          Build the Electron application'

setup: env back-install front-install

env:
	@test -f backend/.env || cp backend/.env.example backend/.env
	@test -f app/.env || cp app/.env.example app/.env

check-uv:
	@command -v uv >/dev/null 2>&1 || { \
		echo 'uv was not found. Add it to Git Bash with:'; \
		echo '  export PATH="$$HOME/.local/bin:$$PATH"'; \
		exit 127; \
	}

back-install: check-uv env
	cd backend && uv sync --system-certs

front-install: env
	cd app && npm install

back: check-uv env
	cd backend && uv run python main.py

backend: back

front: env
	cd app && npm run dev

frontend: front

dev:
	$(MAKE) --no-print-directory -j2 back front

build:
	cd app && npm run build
