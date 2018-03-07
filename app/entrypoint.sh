#!/bin/sh

if $APM_ENABLED; then
    echo "APM tracing enabled: $APM_APP_NAME"
    # start our server through ddtrace-run, which will allow us to see apm tracing in datadog
    ddtrace-run uwsgi /config/uwsgi.yaml
else
    echo "APM tracing disabled"
    uwsgi /config/uwsgi.yaml
fi
