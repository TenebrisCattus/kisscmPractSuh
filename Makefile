.PHONY: run test clean

run:
	python3 src/main.py

test:
	pytest tests/

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete