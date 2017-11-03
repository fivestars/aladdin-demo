# Style Guidelines

## Naming Conventions

| | Description | Example |
|---|---|---|
| GitHub | A repo name that contains a collection of things that work together | aladdin-demo |
| Project | Same as Git repository name | aladdin-demo |
| Dockerfiles | Named "Dockerfile" and reside within the root of associated app folder, see directory structure of more info | commands_app/Dockerfile |
| Helm Chart Name | Same as Git repository name | aladdin-demo |
| Yaml file names | Reside in appropriate app folder, \<kubenetes object type\>.yaml. If there are multiple of the same type of object in the app, then include component name. | redis/service.yaml, server/nginx.configMap.yaml, server/uwsgi.configMap.yaml |
| k8s label: project | Same as Helm Chart Name, accessed with {{ .Chart.Name }} | aladdin-demo |
| k8s label: name | Name of component in the project - should match the first part of the file name. Format: \<project name\>-\<component name\> | aladdin-demo-redis |
| k8s label: app | Same as the label "name". This is redundant and should be removed soon. However at present, Aladdin is dependent on this label. | aladdin-demo-elasticsearch |
| k8s label githash | Should be {{ .Values.deploy.imageTag }} - which is set automatically by aladdin | dab4923c44 |


## Directory Structure

### Build Files
The recommended structuring for build files is to have each project component directory hold their own build files. This way, each app manages its own `.dockerignore`, and it is easier to see which build files go with which project. It is also mirrors our recommended structuring style of helm files. 

Aladdin currently only takes one build script, so there would still need a build script to rule them all for now, which can be located in the root directory. Usually just this one build script can build all the docker images, but if the project needs it, each app directory can also manage their own build script and have the main script call them.

- lamp.json
- build
  - build_docker.sh
- /server
  - .dockerignore
  - requirements.txt
  - Dockerfile
  - entrypoint.sh
  - build_docker.sh
  - /code stuff
- /commands
  - .dockerignore
  - requirements.txt
  - Dockerfile
  - entrypoint.sh
  - build_docker.sh
  - /code stuff
- /helm
### Helm Files
The recommended Helm directory structure is demonstrated below, with /helm at the root. Notably, within the /templates folder, have subdirectories for files specific to each component of the project, as well as a shared directory for shared files such as configMaps.

With this subdirectory structure, the names of the yaml file no longer need to be <project name>-<component name>.deploy.yaml, as it will be reflected in the directory structure. We will just opt for the shorter 'deploy.yaml' etc. A possible exception is for configMaps containing configuration files, such as nginx or uwsgi configs, since a project component may need multiple of these files and just one configMap.yaml may not suffice. 

- /helm
  - /chartname
    - Chart.yaml
    - values.yaml
    - /values
      - values.DEV.yaml
      - values.STAG.yaml
      - values.PROD.yaml
      - values.LOCAL.yaml
    - /templates
      - /commands
        - deploy.yaml
      - /server
        - _nginx.conf.tpl
        - nginx.configMap.yaml
        - deploy.yaml
        - service.yaml
     - /elasticsearch
        - deploy.yaml
        - service.yaml
        - elasticsearch.configmap.yaml
        - _elasticsearch.yml.tpl
      - /shared
        - configMap.yaml

## Configuration Files
All values should be stored in a values.yaml file. The templates should always reference values using helm variables. Configuration files for non-kubernetes objects, such as an nginx config file or a uwsgi config file, should be located in the template folder with a name that begins with an underscore and ends with ".tpl". This gives the ability to easily change configuration values on the fly, without needing to restart the pod every time.

For example, below is the [\_nginx.conf.tpl](../helm/aladdin-demo/templates/server/_nginx.conf.tpl) file. 
```
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

In order to keep files modularized, we create a ConfigMap, the example below is [server/nginx.configMap.yaml](../helm/aladdin-demo/templates/server/nginx.configMap.yaml).
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Chart.Name }}-nginx
data:
  # desired name for the file
  nginx.conf: {{ include "nginx-config" . | quote }}
```
Under data, we can load the config file under its desired name, and we can attach the chart name. This file can then be mounted in the deploy template for our app, [server/deploy.yaml](../helm/aladdin-demo/templates/server/deploy.yaml), giving the docker container access to it.
```yaml
volumeMounts:
  - mountPath: /etc/nginx/
    name: {{ .Chart.Name }}-nginx
```
This will put /etc/nginx/nginx.conf into the docker container with that absolute path, equivalent to copying over a local nginx.conf file in a Dockerfile. 

## Git Hooks
You may wish to include git hooks in your project, such as style checks or unit tests. It is recommended that you use this [Fivestars git-hooks](https://github.com/fivestars/git-hooks) tool to structure your custom hooks for better readability. We have set up a [.githooks](../.githooks) directory and written a [pre-commit](../.githooks/pre-commit-00-style) hook that installs and runs flake8, a python style checker. Follow the instructions for installing [git-hooks](https://github.com/fivestars/git-hooks) and try to make a commit with bad python code to see it in action.
