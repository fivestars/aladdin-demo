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

## Useful and Important Documentation
- [Style Guidelines](docs/style_guidelines.md)
- [CommandsContainers](docs/commands_containers.md)
- [InitContainers](docs/init_containers.md)
- [Using Nginx](docs/nginx.md)
- [Using Redis](docs/redis.md)
- [Autoscaling](docs/autoscaling.md)
