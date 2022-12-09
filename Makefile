SHELL := /bin/bash
FULL_PATH := $(shell pwd)
ENV := $(shell basename $(FULL_PATH))

.PHONY: init-env
init-env:
	conda create --yes -n $(ENV) python=3.10
	. ~/.bash_profile && conda activate $(ENV) && pip install -r requirements.txt
