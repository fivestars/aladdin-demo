Aladdin Installation

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
This file is essentially providing aladdin with a roadmap to your project. The [lamp.json](lamp.json) file for this demo project looks like this.

    {
        "name": "aladdin-demo",
        "build_docker": "./build/build_docker.sh",
        "helm_chart": "./helm/aladdin-demo",
        "docker_images": [
            "aladdin-demo"
        ]
    }
You will need to specify a name, which should be a project name that adheres to the naming guidelines. This name should be used everywhere.

The `build_docker` field should point to where your docker building script is.

The `helm_chart` field should point to your project's helm directory. See [below](#helm) for more details about what should go in this directory.

The `docker_images` field should contain a list of the names of the images your project will be using. Only the custom images that you build need to be specified. External images that are used directly, such as busybox, redis, or nginx, do not need to be in this list.

### helm 
It is highly recommended that you take a look at the official [Helm Chart Template Guide](https://docs.helm.sh/chart_template_guide/#subcharts-and-global-values), especially if you are unfamiliar with Kubernetes or Helm. It is well written and provides a good overview of what helm is capable of, as well as detailed documentation of sytax. It will help you understand the helm charts in this demo better and allow you to follow along with greater ease. We will also be referencing specific sections of the Helm guide in the rest of this document.
### docker

## Style Guidelines
### Naming Conventions
### Directory Structure
### Configuration Files
All values should be stored in a values.yaml file. The templates should always reference values using helm variables. Configuration files for non-kubernetes objects, such as an nginx config file or a uwsgi config file, should be located in the template folder with a name that begins with an underscore and ends with ".tpl". This gives the ability to easily change configuration values on the fly, without needing to restart the pod every time.

For example, below is the [\_nginx.conf.tpl](helm/aladdin-demo/templates/_nginx.conf.tpl) file. 

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

This creates a named template that we can reference elsewhere with the give name `nginx-config`. If you want to know more about how this works, check out [this section](https://docs.helm.sh/chart_template_guide/#declaring-and-using-templates-with-define-and-template) in the Helm Chart Template Guide.

In order to keep files modularized, we create a ConfigMap, the example below is [aladdin-demo-nginx.configMap.yaml](helm/aladdin-demo/templates/aladdin-demo-nginx.configMap.yaml).

    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: {{ .Chart.Name }}-nginx
    data:
      # desired name for the file
      nginx.conf: {{ include "nginx-config" . | quote }}

Under data, we can load the config file under its desired name, and we can attach the chart name. This file can then be mounted in the deploy template for our app, [aladdin-demo.deploy.yaml](helm/aladdin-demo/templates/aladdin-demo.deploy.yaml), giving the docker container access to it.

    volumeMounts:
      - mountPath: /etc/nginx/
        name: {{ .Chart.Name }}-nginx

This will put /etc/nginx/nginx.conf into the docker container with that absolute path, equivalent to copying over a local nginx.conf file in a Dockerfile. 

## InitContainers
InitContainers are generally lightweight containers that contain a few simple instructuions. The initContainers must run and successfully exit before the pod can start. If it fails, Kubernetes will keep trying to restart the initContainers until it is successful. You can have multiple initContainers, and they will simply execute one by one in the order they are defined. We will look at specifi examples of how we use initContainers with [nginx](#nginx-initcontainer) and [redis](#redis-initcontainer) in the secions below.

## Using NGINX
We demonstrate running an nginx container within the same pod as the aladdin-demo app. Our template sets up nginx as a simple proxy server that will listen to all traffic on a port and forward it to the falcon app. We specify the nginx values in the [values.yaml](helm/aladdin-demo/values.yaml) file.

    app:
      # default to the python app port
      port: 7892
      nginx:
        use: false
        port: 8001
        
Set the `use` field to `true`. This is all you need to do to see nginx work, you can verify this by restarting the app with `aladdin restart`. Navigate to the aladdin-demo service pod in the Kubernetes dashboard and you should be able to see two containers running. Read on for how we did it. 

Since we are just using the `nginx:1.12-alpine` image without modifications, there is no need to create a separate Dockerfile for it. 

We add the nginx configuration files using the templating method described in the [Configuration Files](#configuration-files) section. We then add another container for nginx in [aladdin-demo.deploy.yaml](helm/aladdin-demo/templates/aladdin-demo.deploy.yaml).

          - name: {{ .Chart.Name }}-nginx
            image: nginx:1.12-alpine
            ports: 
              - containerPort: {{ .Values.app.nginx.port }}
                protocol: TCP
            volumeMounts:
              - mountPath: /etc/nginx/
                name: {{ .Chart.Name }}-nginx

In the [aladdin-demo.service.yaml](helm/aladdin-demo/templates/aladdin-demo.service.yaml), we expose the nginx port for the pod so that all incoming requests get routed to nginx first. 

### Nginx InitContainer
We have added a simple initContainer for nginx.

In the same [aladdin-demo.deploy.yaml](helm/aladdin-demo/templates/aladdin-demo.deploy.yaml) file, we add a field for initContainers.

      initContainers:
    {{ if .Values.app.nginx.use }}
      # writes a short message into index.html into a mounted volume file shared by nginx
      # this will be the default page that shows up when sending get requests to nginx that
      # are not forwarded to uWSGI
      - name: install
        image: busybox
        command: ["sh", "-c", "printf '\n You have reached NGINX \n \n' > /work-dir/index.html"]
        volumeMounts:
        - name: workdir
          mountPath: "/work-dir"
    {{ end }}

This initContainer, which we named `install`, only needs to run a simple shell command that writes a short welcome message into a file. Therefore, it doesn't need a docker image that has any application code, it can just use a lightweight image, in this case [busybox](https://hub.docker.com/_/busybox/). 

Since the index.html file needs to be shared with the nginx container, we put it into a shared volume called `workdir`. This volume also needs to be added in the volumes field for the deployment

        - name: workdir 
          emptyDir: {}
We also mounth this volume in the nginx container

       volumeMounts:
      # mount html that should contain an index.html file written by the init container
      - mountPath: /usr/share/nginx/html
        name: workdir

This is all that is needed for this simple initContainer to run. We can verify that it wrote the `index.html` file by simpling running `$ curl $(minikube service --url aladdin-demo)`, which should return `You have reached NGINX`.

## Using Redis
We demonstrate running a second pod with a redis container and having the aladdin-demo app retreive data from it upon request. Our template creates a redis server, then creates a connection to it in the falcon app using the redis-py client. Similar to the nginx example, we specify redis values in [values.yaml](helm/aladdin-demo/values.yaml).

    redis:
      create: false
      port: 6379
      containerPort: 6379
      
Changing the `create` field to `true` and restarting the app with `aladdin restart` will show you redis at work. **TODO** Currently redis startup takes about 130 seconds, so wait a bit and then verify that redis is working by curling the redis endpoint of the app. 
    
    $ curl $(minikube service --url aladdin-demo)/app/redis 
    
This should return `I can show you the world from Redis`. In the Kubernetes dashboard, you should also see two pods, one named `aladdin-demo` and the other named `aladdin-demo-redis`. We will detail how everything fits together below. 

We are using the `redis:2.8` image with no modifications, so a Dockerfile is not needed. Eventually our python app will be needing information about redis, so we can store this information as key-value pairs the [configMap](helm/aladdin-demo/templates/aladdin-demo.configMap.yaml).

    data:
      REDIS_HOST: {{ .Chart.Name }}-redis
      REDIS_PORT: {{ .Values.redis.port | quote }}
      REDIS_CREATE: {{ .Values.redis.create | quote }}

In [aladdin-demo.deploy.yaml](helm/aladdin-demo/templates/aladdin-demo.deploy.yaml), we load the data from the [configMap](helm/aladdin-demo/templates/aladdin-demo.configMap.yaml) as environment variables. This allows the python app to access the redis information through `os.environ["KEY"]`, as we will see later. 

    envFrom:
      - configMapRef:
          name: {{ .Chart.Name }}

Since we are putting redis in its own pod, it needs its own deployment and service objects. Following our naming convention for helm charts, we create [aladdin-demo-redis.deploy.yaml](helm/aladdin-demo/templates/aladdin-demo-redis.deploy.yaml) and [aladdin-demo-redis.service.yaml](helm/aladdin-demo/templates/aladdin-demo-redis.service.yaml).

With these files, the redis pod will successfully deploy in Kubernetes. Now we just need to connect it with the python app. We create a simple connection in [redis_connection.py](redis_connection.py) called `redis_conn`, and populate it with a simple message. 

    import redis
    import os

    redis_conn = None
    if os.environ["REDIS_CREATE"] == "true":
        redis_conn = redis.StrictRedis(
                    host=os.environ["REDIS_HOST"],
                    port=os.environ["REDIS_PORT"],
                )
        redis_conn.set('msg', '\n I can show you the world from Redis \n \n')
        
In [run.py](run.py), we define a redis resource and add it to the falcon api.

    import falcon
    from redis_util.redis_connection import redis_conn
    
    class RedisResource(object):
        def on_get(self, req, resp):
            resp.status = falcon.HTTP_200
            msg = redis_conn.get('msg')
            resp.body = (msg)

    app = falcon.API()

    if redis_conn:
        app.add_route('/app/redis', RedisResource())

### Redis InitContainer
For this demo app, there is only one line of data in our redis database, so doing the population in the app will not cause any noticable problems. However, it is more likely the case that your database will have a much larger dataset. In this case, we can leverage initContainers to ensure redis is fully populated and ready to serve before starting up the main application. This avoids errors in the case where the app is running and receiving requests but the database is not, resulting in returned errors. By blocking the app, anyone that tries to connect to the app's endpoint will be told `Waiting, endpoint for service is not ready yet...`, and will retry after a short sleep instead of returning an error.

We demonstrate this by having two initContainers. The first one checks to see that the redis service is running, and the second one populates the database. 

Similar to the nginx initContainer, all this requires is a definition of a name, image, and command. In order to keep files cleaner, we put the definitions in [\_redis_init.tpl](helm/aladdin-demo/templates/_redis_init.tpl), using the same `define` method for templates. 

    {{ define "redis_check" -}}
    {{ if .Values.redis.create }}
    - name: {{ .Chart.Name }}-redis-check
      image: busybox
      command:
      - 'sh'
      - '-c'
      - 'until nslookup {{ .Chart.Name }}-redis; do echo waiting for redis pod; sleep 2; done;'
    {{ end }}
    {{ end }}

    ---

    {{ define "redis_populate" -}}
    {{ if .Values.redis.create }}
    - name: {{ .Chart.Name }}-redis-populate
      image: {{ .Values.deploy.ecr }}{{ .Chart.Name }}:{{ .Values.deploy.imageTag }}
      command:
      - 'python3'
      - 'redis_util/redis_populate.py'
      envFrom:
        - configMapRef:
            name: {{ .Chart.Name }}
    {{ end }}
    {{ end }}

Then, in [aladdin-demo.deploy.yaml](helm/aladdin-demo/templates/aladdin-demo.deploy.yaml), we `include` them, which will simply copy and paste the code defined earlier in the following location. We need to manually indent it to ensure it is valid yaml.
    
    initContainers:
    # initContainer that checks that redis contianer is up and running
    {{ include "redis_check" . | indent 6 }}
    # initContainer that populates redis, only runs if the previous one terminates successfully
    {{ include "redis_populate" . | indent 6 }}

These initContainers will run before the pod starts. 

## Project Specific Commands
[Confluence page](https://fivestars.atlassian.net/wiki/spaces/DEV/pages/49257521/Project+Specific+Commands+Architecture)
We can run project-specific commands through aladdin by creating a dedicated pod for managing the execution of commands. The architecture and design are highlighted in the confluence page above.

We will demonstrate by implementing a simple `status` command for aladdin-demo, which simply does a dns lookup for the aladdin-demo pod and the redis pod, and prints out their status. You can execute this command by running `$ aladdin cmd aladdin-demo status`.

We start by creating [aladdin-demo-commands.Dockerfile](docker/aladdin-demo-commands.Dockerfile), which inherits from the `commands_base` image from aladdin.

    FROM 281649891004.dkr.ecr.us-east-1.amazonaws.com/aladdin:commands_base
    COPY commands_app/requirements.txt ./requirements.txt
    RUN pip install -r requirements.txt
    COPY commands_app/commands commands
    
We then add the following line to the [build_docker.sh](build/build_docker.sh) script.

    #aws login because we are pulling from ecr for base image
    $(aws --profile sandbox ecr get-login)
    docker_build "aladdin-demo-commands" "docker/aladdin-demo-commands.Dockerfile" "."
    
The code for the commands should live in [commands](commands_app/commands/) under a commands_app directory, and each command needs to have a separate file with the same name as the command. For example, we are writing a `status` command, so we create [status.py](commands_app/commands/status.py). 

In each command file, in addition to a function that actually executes the command, a `parse_args` function must be defined in order for aladdin to find and execute the right command. Our status function simply does a dns lookup for the aladdin-demo pod and the redis pod, and prints out their status.

    def parse_args(sub_parser):
        subparser = sub_parser.add_parser("status", help="Report on the status of the application")
        subparser.set_defaults(func=print_status)

    def print_status(arg):
    """ Prints the status of the aladdin-demo pod and the redis pod """
    if socket.gethostbyname("aladdin-demo"):
        print("Aladdin demo app up and ready")
    else:
        print("Cannot find aladdin demo app, possible errors may have occurred")
    if socket.gethostbyname("aladdin-demo-redis"):
        print("Redis server up and ready")
    else: 
        print("Cannot find redis server")
        
Finally, a deployment must be added, which will give the specifications for creating the commands pod. See [aladdin-demo-commands.deploy.yaml](helm/aladdin-demo/templates/aladdin-demo-commands.deploy.yaml) for our example.
