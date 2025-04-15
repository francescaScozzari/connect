.DEFAULT_GOAL := help

.PHONY: behave
behave:  ## Run behave test
	./scripts/behave.sh

.PHONY: check
check:  ## Check code formatting and import sorting
	./scripts/check.sh

.PHONY: collectstatic
collectstatic:  ## Django collectstatic
	python3 -m manage collectstatic --clear --link --noinput

.PHONY: clearpybliometricscache
clearpybliometricscache:  ## Clear pybliometrics cache directory
	rm --force --recursive /dev/shm/.cache/pybliometrics

.PHONY: compilemessages
compilemessages:  ## Django compilemessages
	python3 -m manage compilemessages

.PHONY: coverage
coverage:  ## Run coverage
	./scripts/coverage.sh

.PHONY: createsuperuser
createsuperuser:  ## Django createsuperuser
	python3 -m manage createsuperuser --noinput

.PHONY: dumpgroups
dumpgroups:  ## Django dump auth.Group data
	python3 -m manage dumpdata auth.Group --natural-foreign --natural-primary --output connect/fixtures/groups.json

.PHONY: dumpuniversities
dumpuniversities:  ## Django dump universities data
	python3 -m manage dumpdata universities --natural-foreign --natural-primary --output universities/fixtures/universities.json

.PHONY: fix
fix:  ## Fix code formatting, linting and sorting imports
	python3 -m black .
	python3 -m ruff --fix .
	python3 -m mypy --no-site-packages .

.PHONY: flush
flush:  ## Django flush
	python3 -m manage flush --noinput

.PHONY: graph_models
graph_models:  ## Django generate graph models
	python3 -m manage graph_models --output models.svg

.PHONY: loadgroups
loadgroups:  ## Django load auth.Group data
	python3 -m manage loaddata connect/fixtures/groups.json

.PHONY: loaduniversities
loaduniversities:  ## Django load universities data
	python3 -m manage loaddata universities/fixtures/universities.json

.PHONY: local
local: pip_update  ## Install local requirements and dependencies
	python3 -m piptools sync requirements/local.txt

.PHONY: messages
messages:  ## Django makemessages
	python3 -m manage makemessages --add-location file --ignore requirements --ignore htmlcov --ignore features --ignore gunicorn.conf.py --locale it

.PHONY: migrate
migrate:  ## Django migrate
	python3 -m manage migrate --noinput

.PHONY: migrations
ifeq ($(name),)
migrations: ## Django makemigrations with optional `name="migration_name app_name"`
	python3 -m manage makemigrations --no-header
else
migrations:
	python3 -m manage makemigrations --no-header --name $(name)
endif

.PHONY: outdated
outdated:  ## Check outdated requirements and dependencies
	python3 -m pip list --outdated

.PHONY: pip
pip: pip_update  ## Compile requirements
	python3 -m piptools compile --generate-hashes --no-header --quiet --resolver=backtracking --upgrade --strip-extras --output-file requirements/base.txt requirements/base.in
	python3 -m piptools compile --generate-hashes --no-header --quiet --resolver=backtracking --upgrade --strip-extras --output-file requirements/common.txt requirements/common.in
	python3 -m piptools compile --generate-hashes --no-header --quiet --resolver=backtracking --upgrade --strip-extras --output-file requirements/remote.txt requirements/remote.in
	python3 -m piptools compile --generate-hashes --no-header --quiet --resolver=backtracking --upgrade --strip-extras --output-file requirements/test.txt requirements/test.in
	python3 -m piptools compile --generate-hashes --no-header --quiet --resolver=backtracking --upgrade --strip-extras --output-file requirements/local.txt requirements/local.in

.PHONY: pip_update
pip_update:  ## Update requirements and dependencies
	python3 -m pip install --quiet --upgrade pip~=23.3.0 pip-tools~=7.3.0 setuptools~=69.0.0 wheel~=0.42.0

.PHONY: precommit
precommit:  ## Fix code formatting, linting and sorting imports
	python3 -m pre_commit run --all-files

.PHONY: precommit_update
precommit_update:  ## Update pre_commit
	python3 -m pre_commit autoupdate

.PHONY: pytest
pytest: clearpybliometricscache ## Run debugging test
	python3 -m pytest --capture=no --dc=Testing --durations 10

.PHONY: remote
remote: pip_update  ## Install remote requirements and dependencies
	python3 -m piptools sync requirements/remote.txt

.PHONY: report
report:  ## Run coverage report
	./scripts/report.sh

.PHONY: runserver
runserver:  ## Django run
	python3 -m manage runserver 0:8000

.PHONY: shellplus
shellplus:  ## Run shell_plus
	python3 -m manage shell_plus

ifeq (simpletest,$(firstword $(MAKECMDGOALS)))
  simpletestargs := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(simpletestargs):;@true)
endif

.PHONY: simpletest
simpletest: clearpybliometricscache ## Run debugging test
	# You can pass more arguments as follows:
	# make simpletest -- --debug-sql --failfast --keepdb --pdb --verbosity 2 path.to.TestClass
	PYB_CONFIG_FILE="./scopus/tests/config/pybliometrics.cfg" python3 -m manage test --configuration=Testing --shuffle --timing $(simpletestargs)

.PHONY: test
test: clearpybliometricscache ## Run test
	./scripts/test.sh

.PHONY: update
update: pip precommit_update ## Run update

.PHONY: help
help:
	@echo "[Help] Makefile list commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
