SHELL := /bin/bash
FULL_PATH := $(shell pwd)
ENV := $(shell basename $(FULL_PATH))

.PHONY: init-env
init-env:
	conda create --yes -n $(ENV) python=3.10
	. ~/.bash_profile && conda activate $(ENV) && pip install -r requirements.txt

.PHONY: check
check:
	mypy --strict --pretty --show-error-codes .
	black --diff --check .
	pylint code

.PHONY: leaderboard
leaderboard:
	python code/leaderboard.py
	git add README.md
	git commit -m "(auto) Update leaderboard"
	git push
