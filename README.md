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

We will go over how to get the base project working with Aladdin. See the [Useful and Important Documentation](#useful-and-important-documentation) section for a detailed guide on each of the extra integrated components.

## Aladdin Files
These components are required for aladdin to run a project

### lamp.json
This file is essentially providing aladdin with a roadmap to your project. The [lamp.json](lamp.json) file for this demo project looks like this.

    {
        "name": "aladdin-demo",
        "build_docker": "./build/build_docker.sh",
        "helm_chart": "./helm/aladdin-demo",
        "docker_images": [
            "aladdin-demo",
            "aladdin-demo-commands"
        ]
    }
You will need to specify a name, which should be a project name that adheres to the naming guidelines defined in [Style Guidelines](docs/style_guidelines.md). This name should be used everywhere.

The `build_docker` field should point to where your docker building script is.

The `helm_chart` field should point to your project's Helm directory. See [below](#helm) for more details about what should go in this directory.

The `docker_images` field should contain a list of the names of the images your project will be using. Only the custom images that you build need to be specified. External images that are used directly, such as busybox, redis, or nginx, do not need to be in this list.

### Docker
Your project will need to be running in Docker containers, which only require a Dockerfile and a build script. It may be beneficial to get a basic understanding of Docker from the [Official Get Started Documentation](https://docs.docker.com/get-started/). 

This is the [aladdin-demo.Dockerfile](app/docker/aladdin-demo.Dockerfile). It starts from a base image of `alpine:3.6` and installs everything in `requirements.txt`, copies over the necessary code, and adds an entrypoint, which is the command that runs when the container starts up. The comments in the code should explain each command.

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

The [requirements.txt](app/requirements.txt) simply specify certain versions of libraries that are required for the app to run. This is what we have in our requirements file.

    redis==2.10.6
    falcon==1.3.0
    uwsgi==2.0.15

### Helm 
Helm charts are the main way to specify objects to create in Kubernetes. It is highly recommended that you take a look at the official [Helm Chart Template Guide](https://docs.helm.sh/chart_template_guide/), especially if you are unfamiliar with Kubernetes or Helm. It is well written and provides a good overview of what helm is capable of, as well as detailed documentation of sytax. It will help you understand the helm charts in this demo better and allow you to follow along with greater ease. We will also be referencing specific sections of the Helm guide in the rest of this document.


## Useful and Important Documentation
- [Style Guidelines](docs/style_guidelines.md)
- [CommandsContainers](docs/commands_containers.md)
- [InitContainers](docs/init_containers.md)
- [Using Nginx](docs/nginx.md)
- [Using Redis](docs/redis.md)
- [Autoscaling](docs/autoscaling.md)
