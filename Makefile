main:
	@echo "hello!"

test:
	pytest .

isort:
	isort --profile=black src tests
