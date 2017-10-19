# Style Guidelines

## Naming Conventions

| | Description | Example |
|---|---|---|
| GitHub | A repo name that contains a collection of things that work together | aladdin-demo |
| Project | Same as Git repository name | aladdin-demo |
| Dockerfiles | TODO | TODO |
| Helm Chart Name | Same as Git repository name | aladdin-demo |
| Yaml file names | \<name of kubernetes object\>.\<kubenetes object type\>.yaml | aladdin-demo.service.yaml |
| configmap name | Should match \<project name\> if used project wide, or match \<project name\>-\<component name\> if only used by that component. | aladdin-demo, aladdin-demo-uwsgi |
| k8s label: project | Same as Helm Chart Name, accessed with {{ .Chart.Name }} | aladdin-demo |
| k8s label: name | Name of component in the project - should match the first part of the file name. Format: \<project name\>-\<component name\> | aladdin-demo-redis |
| k8s label: app | Same as the label "name". This is redundant and should be removed soon. However at present, Aladdin is dependent on this label. | aladdin-demo-elasticsearch |
| k8s label githash | Should be {{ .Values.deploy.imageTag }} - which is set automatically by aladdin | dab4923c44 |


## Directory Structure

## Configuration Files
All values should be stored in a values.yaml file. The templates should always reference values using helm variables. Configuration files for non-kubernetes objects, such as an nginx config file or a uwsgi config file, should be located in the template folder with a name that begins with an underscore and ends with ".tpl". This gives the ability to easily change configuration values on the fly, without needing to restart the pod every time.

For example, below is the [\_nginx.conf.tpl](../helm/aladdin-demo/templates/_nginx.conf.tpl) file. 
```json
{{/* Config file for nginx */}}
{{ define "nginx-config" -}}
events {
    worker_connections 4096;
}
http { 
    server {
    listen {{ .Values.app.nginx.port }};
        location /app {
            proxy_pass http://localhost:{{ .Values.app.port}};
        }
        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
}
{{ end }}
```
This creates a named template that we can reference elsewhere with the give name `nginx-config`. If you want to know more about how this works, check out [this section](https://docs.helm.sh/chart_template_guide/#declaring-and-using-templates-with-define-and-template) in the Helm Chart Template Guide.

In order to keep files modularized, we create a ConfigMap, the example below is [aladdin-demo-nginx.configMap.yaml](../helm/aladdin-demo/templates/aladdin-demo-nginx.configMap.yaml).
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Chart.Name }}-nginx
data:
  # desired name for the file
  nginx.conf: {{ include "nginx-config" . | quote }}
```
Under data, we can load the config file under its desired name, and we can attach the chart name. This file can then be mounted in the deploy template for our app, [aladdin-demo.deploy.yaml](../helm/aladdin-demo/templates/aladdin-demo.deploy.yaml), giving the docker container access to it.
```yaml
volumeMounts:
  - mountPath: /etc/nginx/
    name: {{ .Chart.Name }}-nginx
```
This will put /etc/nginx/nginx.conf into the docker container with that absolute path, equivalent to copying over a local nginx.conf file in a Dockerfile. 
