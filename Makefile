VERSION := $(shell grep __version__ tantrum/version.py | cut -d\" -f2)

.PHONY: docs build
env_init:
	pipenv install --dev --skip-lock

env_reset:
	$(MAKE) clean_env
	$(MAKE) env_init

pip_upgrade:
	pip --version
	python --version
	pip install --upgrade pip disttools pipenv

flake:
	pipenv run pip install --quiet --upgrade flake8
	pipenv run flake8 --max-line-length 88 --max-complexity=10 .

black:
	pipenv run pip install --quiet --upgrade black
	pipenv run black .

build:
	$(MAKE) flake
	$(MAKE) black
	$(MAKE) clean_dist

	pipenv run pip install --quiet --upgrade --requirement requirements-build.txt

	# Building Source and Wheel (universal) distribution…
	pipenv run python setup.py sdist bdist_wheel --universal

	# twine checking
	pipenv run twine check dist/*

clean_files:
	find . -type d -name "__pycache__" | xargs rm -rf
	find . -type f -name ".DS_Store" | xargs rm -f
	find . -type f -name "*.pyc" | xargs rm -f

clean_pipenv:
	pipenv --rm || true

clean_dist:
	rm -rf build dist tantrum.egg-info

clean_test:
	rm -rf .egg .eggs junit-report.xml cov_html .tox .pytest_cache .coverage

clean:
	$(MAKE) clean_dist
	$(MAKE) clean_files
	$(MAKE) clean_test
	$(MAKE) clean_pipenv

git_check:
	# checking for version tag
	@git tag | grep "v$(VERSION)" || (echo "no tag for 'v$(VERSION)'"; false)
	# checking if repo has any changes
	git status

git_tag:
	@git tag "v$(VERSION)"
	@echo Added tag: v$(VERSION), now do:
	@echo git push --tags

publish:
	$(MAKE) build
	$(MAKE) git_check
	pipenv run python setup.py upload
