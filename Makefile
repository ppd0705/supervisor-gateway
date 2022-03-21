## install: Install package locally
.PHONT: install
install:
	@bash ./scripts/install.sh

## lint: check syntax and styling
.PHONT: lint
lint:
	@bash ./scripts/lint.sh

## clean: Remove build files
.PHONT: clean
clean:
	@bash ./scripts/clean.sh

## test: Run tests
.PHONT: test
test:
	@bash ./scripts/test.sh

## help: Show this help info.
.PHONT: help
help: Makefile
	@echo "\nUsage: make <TARGET> \n\nTargets:"
	@sed -n 's/^##//p' $< | column -t -s ':' | sed -e 's/^/ /'


