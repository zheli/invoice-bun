.PHONY: install lint test all

install:
	uv sync --extra test

lint:
	uv run ruff check --fix .
	uv run ruff format .
	uv run basedpyright .

test:
	uv run pytest

all: install lint test
