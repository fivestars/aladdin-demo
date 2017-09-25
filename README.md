# Aladdin Installation

## What is Aladdin

**TODO:** Blurb

## Initial Setup

This section describes how to get kubernetes setup and verify that it is working. This includes installing minikube, which is used for local development in kubernetes. 

To set up, just clone the aladdin github repository to get started **TODO:** Confirm once we have public git repository

    $ git clone git@github.com/aladdin/aladdin.git
    $ cd aladdin
    $ ./scripts/infra_k8s_check.sh

The `infra_k8s_check.sh` script checks to see if everything necessary is installed in order to enable local development for various projects and to enable deploying to different environments. 
- If you are missing any dependencies, the script will try and install them for you. 
- This script is also run every time you run the ./aladdin.sh script (more about that script in the Installing our Projects section). 
- __Important:__ Note that this tries to install specific versions of docker, virtual box, minikube, kubectl, and helm that are known to work with aladdin. If you do not want this script to override the version you already have, you will want to alter the versions in the scripts/infra_k8s_check.sh file. However, if you do this, we can not guarantee the behavior of aladdin. 

This will add aladdin to your path as a global alias, allowing you to directly call on aladdin for upcoming commands. You may wish to edit your .bashrc or .bash_profile to execute this command every time you start up a new terminal. 

    $ eval $(./aladdin.sh env) 

**TODO:**[Our common issues page]

# Building a Project
The aladdin-demo is a template project that will demonstrate how to write an aladdin-compatible project. If you are creating a new project from scratch, it is recommended that you start with this template, which already provides simple integration with uwsgi, falcon, nginx, and redis. **TODO** This document will provide a detailed walkthrough of aladdin-demo, explaining each component and best practice guidelines in project development.

## Aladdin Files
These components are required for aladdin to run a project
### lamp.json
### helm 
It is highly recommended that you take a look at the official [Helm Chart Template Guide](https://docs.helm.sh/chart_template_guide/#subcharts-and-global-values), especially if you are unfamiliar with Kubernetes or Helm. It is well written and provides a good overview of what helm is capable of, as well as detailed documentation of sytax. It will help you understand the helm charts in this demo better and allow you to follow along with greater ease. We will also be referencing specific sections of the Helm guide in the rest of this document.
### docker

## Style Guidelines
### Naming Conventions
### Directory Structure
### Configuration Files
All values should be stored in a values.yaml file. The templates should always reference values using helm variables. Configuration files for non-kubernetes objects, such as an nginx config file or a uwsgi config file, should be located in the template folder with a name that begins with an underscore and ends with ".tpl". 

For example, below is the `_nginx.conf.tpl` file located under the templates folder in the aladdin demo folder in the helm directory. 

    {{/* Config file for nginx */}}
    {{ define "nginx-config" -}}
    events {
        worker_connections 4096;
    }
    http { 
        server {
        listen {{ .Values.app.nginx.port }};
            location / {
                proxy_pass http://localhost:{{ .Values.app.port}};
            }
        }
    }
    {{ end }}   
This creates a named template that we can reference elsewhere with the give name `nginx-config`. If you want to know more about how this works, check out [this section](https://docs.helm.sh/chart_template_guide/#declaring-and-using-templates-with-define-and-template) in the Helm Chart Template Guide.

In order to keep files modularized, **TODO fix wording** we create a ConfigMap.

    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: {{ .Chart.Name }}-nginx-config
    data:
      # desired name for the file
      nginx.conf: {{ include "nginx-config" . | quote }}

Under data, we can load the config file under its desired name, and we can attach the chart name. This file can then be mounted in the deploy template for our app, giving the docker container access to it.

    volumeMounts:
      - mountPath: /etc/nginx/
        name: {{ .Chart.Name }}-nginx-config
 This will put /etc/nginx/nginx.conf into the docker container.

## Using NGINX
We demonstrate running an nginx container within the same pod as the aladdin-demo app. Our template sets up nginx as a simple proxy server that will listen to all traffic on a port and forward it to the falcon app. We specify the nginx values in the [values.yaml](helm/aladdin-demo/values.yaml) file.

    app:
      # default to the python app port
      port: 7892
      nginx:
        use: false
        port: 8001
Change the `use` field to `true`. This is all you need to do to see nginx work, you can verify this by restarting the app with `aladdin restart`. Navigate to the aladdin-demo service pod in the Kubernetes dashboard and you should be able to see two containers running. Read on for how we did it. 

Since we are just using the `nginx:1.12-alpine` image without modifications, there is no need to create a separate Dockerfile for it. 

We add the nginx configuration files using the templating method described in the [Configuration Files](#configuration-files) section. We then add another container for nginx in [aladdin-demo.deploy.yaml](helm/aladdin-demo/templates/aladdin-demo.deploy.yaml).

    {{ if .Values.app.nginx.use }}
          # nginx container
          - name: {{ .Chart.Name }}-nginx
            image: nginx:1.12-alpine
            ports: 
              - containerPort: {{ .Values.app.nginx.port }}
                protocol: TCP
            volumeMounts:
              - mountPath: /etc/nginx/
                name: {{ .Chart.Name }}-nginx-config
    {{ end }}

In the [aladdin-demo.service.yaml](helm/aladdin-demo/templates/aladdin-demo.service.yaml), we expose the nginx port for the pod so that all incoming requests get routed to nginx first. 

## Using Redis
