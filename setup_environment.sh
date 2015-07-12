#!/usr/bin/env bash

HELP="usage: $0 [options]
Options:
-v  : Run in verbose mode
-l  : Configure the API instance as a leaf server (This is the default)
-r  : Configure the API instance as a root server
-d  : Configure the API instance in development mode
-p  : Configure the API instance in production mode (This is the default)
-h  : Print this help message"

# Globals
VERBOSE=false
SERVER_TYPE=leaf
SERVER_MODE=production

# Parse options
while getopts "vlrdph" OPTION; do
    case $OPTION in
        v) VERBOSE=true ;;
        l) SERVER_TYPE=leaf ;;
        r) SERVER_TYPE=root ;;
        d) SERVER_MODE=development ;;
        p) SERVER_MODE=production ;;
        h) echo "$HELP"; exit 0 ;;
    esac
done

# Display selected run configuration
$VERBOSE && echo "Selected $SERVER_TYPE server type"
$VERBOSE && echo "Selected $SERVER_MODE server mode"

# If we are not in the directory that contains this script, switch to the
# directory that contains this script
if [[ $0 =~ "/" ]]; then
    $VERBOSE && echo "Changing to script directory"
    cd ${0%/*}
fi

if [[ ! -d "./env" ]]; then
    if [[ ! $TRAVIS ]]; then
        $VERBOSE && echo "Creating virtual environment"
        if $VERBOSE; then
            virtualenv -p python3 --system-site-packages env
        else
            virtualenv -p python3 --system-site-packages env -q
        fi
        $VERBOSE && echo "Activating virtual environment"
        source env/bin/activate
    fi
    $VERBOSE && echo "Installing project dependencies..."
    if $VERBOSE; then
        pip install -r requirements.txt
    else
        pip install -r requirements.txt -q
    fi
fi

# On production servers, install a cron script in /etc/cron.d
if [[ $SERVER_MODE == "production" && -d "/etc/cron.d" ]]; then
    echo "*/5 * * * * $(whoami) source $(pwd -P)/.env && python $(pwd -P)/manage.py runcrons"
fi

# Write the .env file
: > .env # Truncate the file
if [[ ! $TRAVIS ]]; then
    echo "source env/bin/activate" >> .env
fi
echo "export CITYFARM_API_ROOT=$(pwd -P)" >> .env
echo "export CITYFARM_API_SERVER_TYPE=$SERVER_TYPE" >> .env
echo "export CITYFARM_API_SERVER_MODE=$SERVER_MODE" >> .env
echo "export DJANGO_SETTINGS_MODULE=cityfarm_api.settings" >> .env
case $SERVER_MODE in
    development)
        echo "export UWSGI_PROCESSES=1" >> .env
        echo "export UWSGI_MASTER_FIFO=$(pwd -P)/fifo" >> .env
        echo "export UWSGI_HTTP=127.0.0.1:8000" >> .env
        ;;
    production)
        echo "export UWSGI_PROCESSES=4" >> .env
        echo "export UWSGI_MASTER_FIFO=/etc/cityfarm_api_fifo" >> .env
        echo "export UWSGI_HTTP=0.0.0.0:80" >> .env
esac

echo "Wrote configuration to ./.env file. To use it, run \"source .env\""
