.PHONY: help check clean  image run stop

NAME:=dockerzinc
IMAGE:=dockerzinc

define RUN_NOTEBOOK
@echo "Starting notebook server"
@docker run --rm -d -p 127.0.0.1:8888:8888 \
		--name $(NAME) \
		-v $(shell pwd)/source:/home/jovyan/work \
		$(DOCKER_ARGS) \
		$(IMAGE) \
		bash -c "chown jovyan /home/jovyan/work && jupyter trust /home/jovyan/work/*.ipynb && start-notebook.sh $(ARGS)" > /dev/null
@echo "==> wait for server up ..." && sleep 2
@docker exec -it $(NAME) /bin/bash -c "jupyter notebook list"
endef

help:
	@cat README.md

check:
	@which docker > /dev/null || (echo "ERROR: docker not found, please install (or run) docker"; exit 1)
	@docker | grep volume > /dev/null || (echo "ERROR: docker 1.9.0+ required"; exit 1)

image: DOCKER_ARGS?=
image: 
	@docker build --rm $(DOCKER_ARGS) -t $(IMAGE) docker/.

run: DOCKER_ARGS?=
run: check
	@docker image ls | grep $(IMAGE) > /dev/null || (echo "$(IMAGE) image not found"; exit 1)
	$(RUN_NOTEBOOK)

stop:
	@docker container rm -f $(NAME) 2&> /dev/null || true

clean: stop
	@docker rmi $(IMAGE) 2&> /dev/null || true
	@echo "Container and image deleted"