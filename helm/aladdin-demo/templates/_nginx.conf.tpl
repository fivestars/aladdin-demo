{{/* Config file for nginx */}}

# Note: This define name is global, if loading multiple templates with the same name, the last
# one loaded will be used.
{{ define "nginx-config" -}}

# Specify some event configs
events {
    worker_connections 4096;
}

# Create a server that listens on the nginx port

http { 

    server {
    listen {{ .Values.app.nginx.port }};
        
        # Match incoming request uri with "/" and forward them to the uwsgi app
        # All requests will match in this case
        location / {
            proxy_pass http://localhost:{{ .Values.app.port}};
        }
    }
}

{{ end }}
