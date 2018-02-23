#!/bin/sh

# start our server through ddtrace-run, which will allow us to see apm tracing in datadog
ddtrace-run uwsgi /config/uwsgi.yaml

