.DEFAULT_GOAL := help

c = connect_backend
p = shell
.PHONY: django
django_shell:  ## Exec django command
	docker exec -it $(c) python manage.py $(p)

.PHONY: precommit
precommit:  ## Fix code formatting, linting and sorting imports
	python3 -m pre_commit run --all-files

.PHONY: precommit_install
precommit_install:  ## Install pre_commit
	python3 -m pip install pre-commit

.PHONY: precommit_update
precommit_update:  ## Update pre_commit
	python3 -m pre_commit autoupdate

.PHONY: pull
pull:  ## Pull amin on all services
	git checkout main && git pull && \
	cd backend && git checkout main && git pull && \
	cd ../frontend && git checkout main && git pull && \
	cd ..

s =
.PHONY: rebuild
rebuild:  ## Rebuild container
	docker-compose stop $(s) && docker-compose rm -f $(s) && docker-compose up -d --build $(s)

help:
	@echo "[Help] Makefile list commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
