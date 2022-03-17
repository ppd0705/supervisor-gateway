.PHONT: install
install:
	./scripts/install.sh

## lint: check syntax and styling
.PHONT: lint
lint:
	./scripts/lint.sh

.PHONT: clean
clean:
	./scripts/clean.sh


.PHONT: test
test: install
	./scripts/test.sh
