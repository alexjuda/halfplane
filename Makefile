main:
	@echo "hello!"

test:
	pytest . -vv $(OPTS)

isort:
	isort --profile=black src tests
