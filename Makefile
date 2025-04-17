SHELL := /bin/bash  # force bash instead of sh

install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

format:
	@FILES=`find src -type f -name "*.py"`; \
	if [ -z "$$FILES" ]; then \
		echo "No Python files found to format"; \
		exit 0; \
	else \
		python3 -m black $$FILES; \
	fi

lint:
	@FILES=`find src -type f -name "*.py"`; \
	if [ -z "$$FILES" ]; then \
		echo "No Python files found to lint"; \
		exit 0; \
	else \
		python3 -m pylint --disable=R,C,W0621,E0102,E0611,E0401 $$FILES || true; \
	fi

deploy:	
	echo "deployment begun!"

all: install lint format deploy
