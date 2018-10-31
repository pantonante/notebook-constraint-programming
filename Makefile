.PHONY: help check clean remove image run stop

NAME:=dockerzinc

define RUN_NOTEBOOK
@echo "Starting notebook server" && sleep 3
@docker run --rm -d -p 127.0.0.1:$(PORT):8888 \
		--name $(NAME) \
		-v $(shell pwd)/source:/home/jovyan/work \
		$(DOCKER_ARGS) \
		$(IMAGE) \
		bash -c "chown jovyan /home/jovyan/work && jupyter trust /home/jovyan/work/index.ipynb && start-notebook.sh $(ARGS)" > /dev/null
@echo "==> wait for server up ..." && sleep 3
@docker exec -it $(IMAGE) /bin/bash -c "jupyter notebook list"
endef

help:
	@cat README.md

check:
	@which docker > /dev/null || (echo "ERROR: docker not found, please install (or run) docker"; exit 1)
	@docker | grep volume > /dev/null || (echo "ERROR: docker 1.9.0+ required"; exit 1)
	@docker image ls | grep $(NAME) > /dev/null || (echo "$(NAME) image not found"; exit 1)

remove:

clean: remove
	@docker rmi $(NAME) > /dev/null
	@echo "Container and image deleted"

image: DOCKER_ARGS?=
image: IMAGE?=$(NAME)
image: 
	@docker build --rm $(DOCKER_ARGS) -t $(IMAGE) docker/.

run: PORT?=8888
run: NAME?=$(NAME)
run: IMAGE?=$(NAME)
run: check remove
	$(RUN_NOTEBOOK)

stop:
	@docker container rm -f $(NAME) > /dev/null
