#!/bin/sh
export PYTHONPATH=$(pwd)

if [ "$KAMI_BOT_DEBUG_MODE" = "true" ]; then
    echo "Starting bot in hot reload mode..."
    pymon kami/bot_admin/__main__.py
else
    echo "Starting bot in normal mode..."
    python -m kami.bot_admin
fi
