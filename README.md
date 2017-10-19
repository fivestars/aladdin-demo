# Aladdin Installation

## What is Aladdin

**TODO:** Blurb

## Aladdin Setup

This section describes how to get Kubernetes setup and verify that it is working. This includes installing Minikube, which is used for local development in Kubernetes. 

To set up, just clone the Aladdin GitHub repository to get started **TODO:** Confirm once we have public git repository

    $ git clone git@github.com/aladdin/aladdin.git
    $ cd aladdin
    $ ./scripts/infra_k8s_check.sh

The `infra_k8s_check.sh` script checks to see if everything necessary is installed in order to enable local development for various projects and to enable deploying to different environments. 
- If you are missing any dependencies, the script will try and install them for you. 
- This script is also run every time you run the ./aladdin.sh script (more about that script in the Installing our Projects section). 
- __Important:__ Note that this tries to install specific versions of Docker, Virtual Box, Minikube, Kubectl, and Helm that are known to work with Aladdin. If you do not want this script to override the version you already have, you will want to alter the versions in the scripts/infra_k8s_check.sh file. However, if you do this, we can not guarantee the behavior of Aladdin. 

You can add Aladdin to your path as a global alias, allowing you to directly call on aladdin for upcoming commands. You may wish to edit your .bashrc or .bash_profile to execute this command every time you start up a new terminal. 

    $ eval $(./aladdin.sh env) 

**TODO:**[Our common issues page]
 
# Building a Project
The aladdin-demo is a template project that will demonstrate how to write an aladdin-compatible project. If you are creating a new project from scratch, it is recommended that you start with this template, which already provides simple integration with uWSGI, Falcon, NGINX, Redis, and Elasticsearch. This document will provide a detailed walkthrough of aladdin-demo, explaining each component and best practice guidelines in project development.

## Aladdin-demo Setup

Once Aladdin has been installed and set up, you can jump right in to aladdin-demo to see Aladdin in action. 

    $ git clone git@github.com:fivestars/aladdin-demo.git
    $ cd aladdin-demo
    $ aladdin build
    $ aladdin start

This is all you need to do to deploy aladdin-demo! Confirm that it is working by curling the app endpoint and see what aladdin-demo has to say. 

    $ curl $(minikube service --url aladdin-demo)/app
    
      I can show you the world 

We will go over how the base project is working with Aladdin. See the [Useful and Important Documentation](#useful-and-important-documentation) section for a detailed guide on each of the extra integrated components.

## Aladdin Files
These components are required for aladdin to run a project

### lamp.json
This file is essentially providing aladdin with a roadmap to your project. The [lamp.json](lamp.json) file for this demo project looks like this.
```json
{
    "name": "aladdin-demo",
    "build_docker": "./build/build_docker.sh",
    "helm_chart": "./helm/aladdin-demo",
    "docker_images": [
        "aladdin-demo",
        "aladdin-demo-commands"
    ]
}```
You will need to specify a name, which should be a project name that adheres to the naming conventions defined in [Style Guidelines](docs/style_guidelines#naming-conventions.md). This name should be used everywhere.

The `build_docker` field should point to where your docker building script is.

The `helm_chart` field should point to your project's Helm directory. See [below](#helm) for more details about what should go in this directory.

The `docker_images` field should contain a list of the names of the images your project will be using. Only the custom images that you build need to be specified. External images that are used directly, such as busybox, redis, or nginx, do not need to be in this list.

### Docker
Your project will need to be running in Docker containers, which only require a Dockerfile and a build script. It may be beneficial to get a basic understanding of Docker from the [Official Get Started Documentation](https://docs.docker.com/get-started/). 

This is the [aladdin-demo.Dockerfile](app/docker/aladdin-demo.Dockerfile). It starts from a base image of `alpine:3.6` and installs everything in `requirements.txt`, copies over the necessary code, and adds an entrypoint, which is the command that runs when the container starts up. The comments in the code should explain each command.
```dockerfile
FROM alpine:3.6

# install python and pip with apk package manager
RUN apk -Uuv add python py-pip

# uwsgi in particular requires a lot of packages to install, delete them afterwards
RUN apk add --no-cache \
        gettext \
        python3 \
        build-base \
        linux-headers \
        python3-dev

# copies requirements.txt to the docker container
ADD app/requirements.txt requirements.txt

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# clean up environment by deleting extra packages
RUN apk del \
        build-base \
        linux-headers \
        python3-dev

# specify the directory that CMD executes from
WORKDIR /home/aladdin-demo

# copy over the directory into docker container with given path
COPY app /home/aladdin-demo

# Create unprivileged user account
RUN addgroup aladdin-user && \
    adduser -SD -G aladdin-user aladdin-user

# Switch to the unpriveleged user account
USER aladdin-user

# run the application with uwsgi once the container has been created
ENTRYPOINT ["uwsgi", "--yaml", "/config/uwsgi.yaml"]
```
We create and use an unpriviledged user account called aladdin-user, as it is best practice to not run uwsgi as root.

The [requirements.txt](app/requirements.txt) simply specify certain versions of libraries that are required for the app to run. This is what we have in our requirements file.

    redis==2.10.6
    falcon==1.3.0
    uwsgi==2.0.15

The docker build script should just call `docker build` on the desired Dockerfiles. We have included some helper functions that make the process easier. Our [build_docker.sh](build/build_docker.sh) looks like this.
```shell
#!/usr/bin/env bash

echo "Building aladdin-demo docker image (~30 seconds)"

BUILD_PATH="$(cd "$(dirname "$0")"; pwd)"
PROJ_ROOT="$(cd "$BUILD_PATH/.." ; pwd)"
PRINT_ONLY="${PRINT_ONLY:-false}"
HASH="${HASH:-local}"
ALL="${ALL:-false}"

print_only_cmd_wrapper() {
    typeset cmd="$1"
    echo "$cmd"
    if ! $PRINT_ONLY; then
        ${cmd}
    fi
}

docker_build() {
    typeset name="$1" dockerfile="$2" context="$3"
    TAG="$name:${HASH}"
    build_cmd="docker build -t $TAG -f $dockerfile $context"
    print_only_cmd_wrapper "$build_cmd"
}
cd "$PROJ_ROOT"

docker_build "aladdin-demo" "app/docker/aladdin-demo.Dockerfile" "."

#aws login because we are pulling from ecr for base image
$(aws --profile sandbox ecr get-login)
docker_build "aladdin-demo-commands" "app/docker/aladdin-demo-commands.Dockerfile" "."
```
### Helm 
Helm charts are the main way to specify objects to create in Kubernetes. It is highly recommended that you take a look at the official [Helm Chart Template Guide](https://docs.helm.sh/chart_template_guide/), especially if you are unfamiliar with Kubernetes or Helm. It is well written and provides a good overview of what helm is capable of, as well as detailed documentation of sytax. It will help you understand the helm charts in this demo better and allow you to follow along with greater ease. We will also be referencing specific sections of the Helm guide in other parts of our documentation.

#### Chart.yaml
The Helm charts for this project are located in [helm/aladdin-demo](helm/aladdin-demo). The root of this directory should contain [Chart.yaml](helm/aladdin-demo/chart.yaml), a simple file that should define the name and version of the project. This name will be used a lot in other files, and can be accessed through {{ .Chart.Name }}. The version is the version of your project, and should be updated for each new release in accordance to the [Semantic Versioning Specification](http://semver.org/).

    apiVersion: v1
    description: A Helm chart for Kubernetes
    name: aladdin-demo
    version: 0.1.0

#### Values.yaml
Also in the root of the Helm directory is a [values.yaml](heml/aladdin-demo/values.yaml) file. This file defines a number of default values that may be overwritten by other environment specific values files. The environment can be specified through Aladdin, which will use the appropriate values file to deploy the project. **TODO add value files for other environments** 
```yaml
# Application configuration
app:
  # default to the python app port
  port: 7892
  nginx:
    use: true
    port: 8001

deploy:
  # number of seconds for the containers to perform a graceful shutdown, after which it is voilently terminated
  terminationGracePeriod: 50
  replicas: 1

redis:
  create: true
  port: 6379
  containerPort: 6379
```
The values in this file can be accessed in other files through {{ .Values.\<value\> }}. For example, {{ .Values.app.port }} will resolve to 7892.

#### Templates
The [templates](helm/aladdin-demo/templates/) directory is for template files. For our base project, we just need a Kubernetes Deployment object and Service object.

In [aladdin-demo.deploy.yaml](helm/aladdin-demo/templates/aladdin-demo.deploy.yaml) we specify the Deployment object for the aladdin-demo app. The file contains a lot of different components for the integration of various other tools, but for the basic app, the deployment should look something like this. 
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: {{ .Chart.Name }}
  labels:
    project: {{ .Chart.Name }}
    name: {{ .Chart.Name }}
    app: {{ .Chart.Name }}
    githash: {{ .Values.deploy.imageTag }}
spec:
  replicas: {{ .Values.deploy.replicas }}
  strategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        project: {{ .Chart.Name }}
        name: {{ .Chart.Name }}
        app: {{ .Chart.Name }}
    spec:
      terminationGracePeriodSeconds: {{ .Values.deploy.terminationGracePeriod }}
      containers:
        # This is a container that runs the falcon aladdin-demo app with uwsgi server
      - name: {{ .Chart.Name }}
        # Docker image for this container
        image: {{ .Values.deploy.ecr }}{{ .Chart.Name }}:{{ .Values.deploy.imageTag }}
        workingDir: /home/{{ .Chart.Name}} 
        # Container port that is being exposed within the node
        ports:
        - containerPort: {{ .Values.app.port }}
          protocol: TCP
        # Mount the configuration file into the docker container
        volumeMounts:
          # Absolute path is used here
          - mountPath: /config/
            name: {{ .Chart.Name }}-uwsgi
      # Specify volumes that will be mounted in the containers
      volumes:
        - name: {{ .Chart.Name }}-uwsgi
          configMap:
            name: {{ .Chart.Name }}-uwsgi
```
We specify the image in spec.template.spec.containers. If using a custom built docker image, the name should be the same name as what it is named in the build docker script. The `{{ .Values.deploy.ecr }}` and `{{ .Values.deploy.imageTag }}` are automatically populated by Aladdin. 

We also mount the configmap for uwsgi using the cofiguration file guidelines specified in [Style Guidelines](docs/style_guidelines.md#configuration-files).

In [aladdin-demo.service](helm/aladdin-demo/templates/aladdin-demo.service.yaml) we specify the Serivce object for aladdin-demo.
```yaml
apiVersion: v1
kind: Service
metadata: 
  name: {{ .Chart.Name }}
  labels:
    project: {{ .Chart.Name }}
    name: {{ .Chart.Name }}
    app: {{ .Chart.Name }}
    githash: {{ .Values.deploy.imageTag }}
spec:
  # Aladdin will fill this in as NodePort which will expose itself to things outside of the cluster
  # This is to highlight difference between public and private service types, and to only use
  # public service types when it truly should be public
  type: {{ .Values.service.publicServiceType | quote }}
  ports:
    - name: http
      port: {{ .Values.app.port }}
  selector:
    # Get the aladdin-demo deployment configuration from aladdin-demo.deploy.yaml
    name: {{ .Chart.Name }}
```
This file should be much simpler compared to the deployment file, since it just sets up a port, in this case a public NodePort and then through a selector, hooks up the deployment object so that it serves this port. 

## Falcon and uWSGI
We set up a very simple Falcon API app that is backed by uWSGI. The falcon app is defined in [run.py](app/run.py) and it simply adds a few endpoints to the api. 
```python
import falcon

class BaseResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = ('\n I can show you the world \n \n')

app = falcon.API()

app.add_route('/app', BaseResource())
```
Our code is in `run.py` and we named our falcon API object `app`, so we specify those things in the uWSGI config file in [\_uwsgi.yaml.tpl](helm/aladdin-demo/templates/_uwsgi.yaml.tpl).
```yaml
{{ define "uwsgi-config" -}}
uwsgi:
  uid: aladdin-user
  gid: aladdin-user
  master: true
  http: : {{ .Values.app.port }}
  wsgi-file: run.py
  callable: app
{{ end }}
```
With these components in place, we have now created a simple project with Aladdin! For documentation on how we integrated other components, look below at [Useful and Important Documentation](#useful-and-important-documentation)!

## Useful and Important Documentation
- [Style Guidelines](docs/style_guidelines.md)
- [Debugging Tips and Tricks](docs/debugging_tips_and_tricks.md)
- [CommandsContainers](docs/commands_containers.md)
- [InitContainers](docs/init_containers.md)
- [Using Nginx](docs/nginx.md)
- [Using Redis](docs/redis.md)
- [Autoscaling](docs/autoscaling.md)
- [Using Elasticsearch with StatefulSet](docs/elasticsearch_statefulset.md)

