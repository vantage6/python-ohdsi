INSTALL_FLAGS :=
PACKAGES = \
	circe \
	cohort-generator \
	database-connector \
	sqlrender

help:
	@echo "install       - install all packages"
	@echo "install-dev   - install all packages in editable mode"
	@echo "build         - build all packages"
	@echo "publish       - publish all packages to pypi, needs USERNAME and"
	@echo "                PASSWORD"

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

