.PHONY: all build install test

all:
	@echo "Possible Commands"
	@echo "   build: Builds BevyFrame"
	@echo "   install: Installs via pip, needs to be built before installing"
	@echo "   test: Starts test server, needs BevyFrame to installed via pip"

build:
	@python3 -m build

install:
	@python3 -m pip uninstall BevyFrame -y
	@cd dist; python3 -m pip install *.whl

test:
	@cd tests; python3 main.py

clean:
	@rm -rfv dist
	@rm -rfv src/BevyFrame.egg-info
	@rm -rfv build