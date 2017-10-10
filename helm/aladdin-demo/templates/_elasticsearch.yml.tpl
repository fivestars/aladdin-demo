{{/* Config file for elasticsearch */}}

{{ define "elasticsearch-config" -}}
http:
  host: 0.0.0.0
transport:
  host: 127.0.0.1
{{ end }}