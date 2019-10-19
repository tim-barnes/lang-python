repo="template-project"
tag="0.1.0"
name="template-project"

DOCKER = DOCKER_BUILDKIT=1 docker
DOCKERFILE = Dockerfile src/**


default: build
.PHONY: FORCE TOOLS default build test test_build debug format lint typecheck
FORCE:

build: $(DOCKERFILE)
	$(DOCKER) build \
		--tag $(repo):latest \
		--tag $(repo):$(tag) \
		.


run: build
	docker run --rm \
		--publish=5000:5000 \
		--name="$(name)" \
		"$(repo)":latest


test_build:
	debug_name="debug-$(name)"
	docker rm -f "$(debug_name)" > /dev/null 2>&1 || true

	$(DOCKER) build \
		--target=test \
		--tag="$(repo):tests" \
		. || exit 1


debug: $(DOCKERFILE) test_build
	$(DOCKER) run -it \
		--name="$(debug_name)" \
		--mount type=bind,source="$(PWD)/src",destination=/app\
		--entrypoint='' \
		"$(repo)":tests \
		bash


test: $(DOCKERFILE) test_build
	$(DOCKER) run -it \
		--name="$(debug_name)" \
		--mount type=bind,source="$(PWD)/src",destination=/app\
		"$(repo)":tests

tools:
	tools_name="tools-$(name)"
	$(DOCKER) build \
		--target=tools \
		--tag="$(repo):tools" \
		. || exit 1


format: $(DOCKERFILE) tools
	$(DOCKER) run -it \
		--name="$(tools_name)" \
		--mount type=bind,source="$(PWD)/src",destination=/app\
		"$(repo)":tools \
		black .

lint: $(DOCKERFILE) tools
	$(DOCKER) run -it \
		--name="$(tools_name)" \
		--mount type=bind,source="$(PWD)/src",destination=/app\
		"$(repo)":tools \
		flake8 --config=/root/tools.ini

typecheck: $(DOCKERFILE) tools
	$(DOCKER) run -it \
		--name="$(tools_name)" \
		--mount type=bind,source="$(PWD)/src",destination=/app\
		"$(repo)":tools \
		mypy --config=/root/tools.ini .

