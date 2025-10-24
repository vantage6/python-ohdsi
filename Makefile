INSTALL_FLAGS :=
PACKAGES = \
	circe \
	cohort-generator \
	database-connector \
	sqlrender \
	feature-extraction \
	common \
	cohort-diagnostics

help:
	@echo "install       - install all packages using uv"
	@echo "install-dev   - install all packages in editable mode using uv"
	@echo "build         - build all packages using uv"
	@echo "publish       - publish all packages to pypi using uv"
	@echo "                Usage: make publish USERNAME=user PASSWORD=pass"
	@echo "set-version   - set the version of all packages, needs VERSION"

set-version:
	echo '"$(VERSION)"' > VERSION


install:
	$(foreach package, $(PACKAGES), \
		cd $(package) && uv pip install $(INSTALL_FLAGS) . && cd ..; \
	)

install-dev:
	make install INSTALL_FLAGS="-e"

build:
	$(foreach package, $(PACKAGES), \
		cd $(package) && uv build . && cd ..; \
	)

publish:
	@if [ -z "$(USERNAME)" ] || [ -z "$(PASSWORD)" ]; then \
		echo "Error: USERNAME and PASSWORD must be set"; \
		echo "Usage: make publish USERNAME=your_username PASSWORD=your_password"; \
		exit 1; \
	fi
	# publish after you have built the packages
	$(foreach package, $(PACKAGES), \
		cd $(package) && uv publish --username $(USERNAME) --password $(PASSWORD) && cd ..; \
	)

