INSTALL_FLAGS :=
PACKAGES = \
	circe \
	cohort-generator \
	database-connector \
	sqlrender \
	feature-extraction \
	common

IMAGE = "harbor2.vantage6.ai/infrastructure/ohdsi-api"
TAG = "latest"
IMAGE_OPTS = "--progress=plain"


help:
	@echo "install       - install all packages"
	@echo "install-dev   - install all packages in editable mode"
	@echo "build         - build all packages"
	@echo "publish       - publish all packages to pypi, needs USERNAME and"
	@echo "                PASSWORD"
	@echo "set-version   - set the version of all packages, needs VERSION"
	@echo "image         - build the docker image"
	@echo "push          - push the docker image to the registry"

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

image:
	docker build -t $(IMAGE):$(TAG) $(IMAGE_OPTS) ./api

push:
	docker push $(IMAGE):$(TAG)



