#!/bin/sh
set -e

if [ -z "$OLLAMA_MODEL" ]; then
	echo "OLLAMA_MODEL is not set"
	exit 1
fi

echo "Starting Ollama server..."
ollama serve &

# Give the daemon a moment to start listening
sleep 2

echo "Ensuring model is available: $OLLAMA_MODEL"
ollama pull "$OLLAMA_MODEL"

# Keep the container alive, foregrounding ollama
wait
