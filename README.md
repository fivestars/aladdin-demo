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

**TODO:**[Our common issues confluence page]

# Building a Project
The aladdin-demo is a template project that will demonstrate how to write an aladdin-compatible project. If you are creating a new project from scratch, it is recommended that you start with this template, which already provides integration with nginx, blank, blank, and blank. **TODO** This document will provide a detailed walkthrough of aladdin-demo, explaining each component and best practice guidelines in project development.

## Aladdin Files
These files are required for aladdin 
### lamp.json
### helm 
### docker

## Using NGINX
We demonstrate running an nginx container within the same pod as the aladdin-demo app. Our template sets up nginx as a simple proxy server that will listen to all traffic on port 80 and forward it to the tornado app. 

The first step is to configure the nginx server. In the `nginx.conf` file under the `nginx` - `config` directories, we specify a server that listens on port 80. For all requests, it will pass it on to port 7892, which the tornado app is listening on. 

Next, we build a docker image in the `nginx.Dockerfile` under the `build` directory. This file simply starts with an existing nginx image and copies over our configurations for it.