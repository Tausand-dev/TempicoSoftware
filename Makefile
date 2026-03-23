.PHONY: dev test build build-bin clean help

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-12s %s\n", $$1, $$2}'

dev: ## Run the GUI app (X11 via WSLg)
	docker compose run --rm dev

test: ## Run tests headlessly (Xvfb)
	docker compose run --rm test

build: ## Build Linux binary → ./dist/SignalViewer
	docker compose run --rm build

build-bin: ## Build Linux binary without Docker → ./dist/SignalViewer
	sudo apt install -y python3.12-venv
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install "pyinstaller>=6.0"
	.venv/bin/pyinstaller src/app/main.py --name SignalViewer --onefile --windowed

build-exe: ## Build Windows .exe → run build-exe.ps1 from PowerShell on Windows
	@echo "ERROR: Cannot build a Windows .exe from WSL2/Linux."
	@echo "Open PowerShell on Windows and run:  .\\build-exe.ps1"
	@exit 1

clean: ## Remove build artifacts and Docker images
	rm -rf dist/ build/ *.spec
	docker compose down --rmi local --volumes --remove-orphans
