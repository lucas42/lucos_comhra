#!/bin/sh
set -e

ollama serve &

# Wait for Ollama to be ready
until ollama list >/dev/null 2>&1; do
	sleep 1
done

# Build the constrained model
ollama create lucos-llama3.2-3b -f /Modelfile

wait