all: build

build:
	uv build

run:
	uv run --with pygame-ce spikegame/main.py

clean:
	rm -rf dist
