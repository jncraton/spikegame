all: build

lint:
	uvx black@24.1.0 --check .

format:
	uvx black@24.1.0 .

build:
	uv build

run:
	uv run --with pygame-ce spikegame/main.py

clean:
	rm -rf dist
