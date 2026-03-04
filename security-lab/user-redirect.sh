#!/bin/bash
CONTAINER_NAME="kali-lab"
if ! sudo docker ps | grep -q "$CONTAINER_NAME"; then
    echo "Error: Container $CONTAINER_NAME is not running" >&2
    exit 1
fi
exec sudo docker exec -it "$CONTAINER_NAME" /bin/bash