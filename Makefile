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
	@echo "install       - install all packages"
	@echo "install-dev   - install all packages in editable mode"
	@echo "build         - build all packages"
	@echo "publish       - publish all packages to pypi, needs USERNAME and"
	@echo "                PASSWORD"
	@echo "set-version   - set the version of all packages, needs VERSION"

set-version:
	echo $(VERSION) > VERSION;


install:
	$(foreach package, $(PACKAGES), \
		cd $(package) && pip install $(INSTALL_FLAGS) . && cd ..; \
	)

install-dev:
	make install INSTALL_FLAGS="-e"

build:
	$(foreach package, $(PACKAGES), \
		cd $(package) && python setup.py sdist bdist_wheel && cd ..; \
	)

publish:
	# publish after you have built the packages
	$(foreach package, $(PACKAGES), \
		cd $(package) && twine upload --repository pypi dist/* \
		-u $(USERNAME) -p $(PASSWORD) --disable-progress-bar && cd ..; \
	)

