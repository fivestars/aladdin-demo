#!/usr/bin/env sh

# Populate the config file before starting the service
envsubst '$NGINX_PORT $UWSGI_PORT' < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf 

sed /etc/nginx/nginx.conf

# Start the service
nginx -g 'daemon off;' &

pid=$!
trap "kill -SIGTERM $pid; wait $pid" SIGTERM
wait $pid