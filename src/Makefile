install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

format:
	@FILES=$(shell find controllers -name "*.py") && \
	if [ -z "$$FILES" ]; then \
		echo "No Python files found to format"; \
		exit 0; \
	else \
		black $$FILES; \
	fi

lint:
	@FILES=$(shell find helpers -name "*.py") && \
	if [ -z "$$FILES" ]; then \
		echo "No Python files found to lint"; \
		exit 0; \
	else \
		pylint --disable=R,C,W0621,E0102,E0611,E0401 $$FILES; \
	fi

deploy:
	echo "deployment begun!"

# test:
# 	CUDA_VISIBLE_DEVICES=-1 coverage run -m pytest -v test_file.py && coverage report

all: install lint format deploy
