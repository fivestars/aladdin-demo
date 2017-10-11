{{/* Config file for elasticsearch */}}

{{ define "elasticsearch-config" -}}
discovery:
  zen.minimum_master_nodes: 1
script.inline: true
xpack:
  security.enabled: false
  ml.enabled: false
  graph.enabled: false
  monitoring.enabled: false
  watcher.enabled: false

cluster.info.update.interval: "30m"
# path:
#   data: /data/data
#   logs: /data/log

# This allows other pods in the kubernetes cluster to connect to elasticsearch
network.host: 0.0.0.0

{{ end }}