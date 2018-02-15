#!/bin/sh

# start our server through ddtrace-run, which will allow us to see apm tracing in datadog
DATADOG_TRACE_DEBUG=true DATADOG_TRACE_AGENT_HOSTNAME=datadog-agent-apm.kube-system ddtrace-run uwsgi /home/config/uwsgi.yaml
