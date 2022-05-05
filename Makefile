main:
	@echo "hello!"

test:
	pytest . $(OPTS)

isort:
	isort --profile=black src tests
