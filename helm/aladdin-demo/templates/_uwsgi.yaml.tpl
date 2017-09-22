{{/* Config file for uwsgi */}}

# Note: This define name is global, if loading multiple templates with the same name, the last
# one loaded will be used.
{{ define "uwsgi-config" -}}
uwsgi:
  http: :7892
  wsgi-file: run.py
  callable: app

{{ end }}