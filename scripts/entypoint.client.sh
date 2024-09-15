#!/bin/sh
export PYTHONPATH=$(pwd)

if [ "$DEBUG_MODE" = "true" ]; then
    echo "Starting bot in hot reload mode..."
    pymon kami/bot_client/__main__.py
else
    echo "Starting bot in normal mode..."
    python -m kami.bot_client
fi
