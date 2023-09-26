#!/usr/bin/env bash

# Clean docker images
# Keep only the last two images per service fetched from the registry.

# clean frontend images
for image in $(docker images --format "{{.Repository}}:{{.Tag}}" | grep frontend | sed -n '1!p' | sed -n '1!p'); do docker rmi "$image"; done

# clean backend images
for image in $(docker images --format "{{.Repository}}:{{.Tag}}" | grep backend | sed -n '1!p' | sed -n '1!p'); do docker rmi "$image"; done
