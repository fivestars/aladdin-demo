# Debugging Tips and Tricks

Here are some useful tips and tricks to help you debug your application.

## Shell into a Kubernetes Container
Often times when things are behaving strangly, it may be very beneficial to shell into the container to poke around, check that the expected volumes have all been mounted in the correct places, or run some commands directly. Aladdin has a command to help with this. 

### Aladdin Connect
Connect is one of aladdin's commands used to connect to a bash prompt of containers
This command can be called from anywhere.
This command finds the pods related to a supplied deployment name. If only one pod with a single container is found, the `kubectl exec -it /bin/bash` command is sent directly to the pod.
If multiple pods-container pairs are found that contain the supplied deployment name, they are all listed, and an index must be chosen. 


Usage: `aladdin [-c <CLUSTER>] [-n <NAMESPACE>] connect deployment`
- if deployment is not supplied, show all possible pod/container pairs
- can be used with `-c` and `-n` to connect to containers in other clusters

```
  > aladdin connect aladdin-demo

Available:
----------
0: pod aladdin-demo-3016337494-v91pp; container aladdin-demo
1: pod aladdin-demo-3016337494-v91pp; container aladdin-demo-nginx
Choose an index:  0
```
One thing to keep in mind is that this only works for running containers. So if your container has encountered an error and is not currently running, you will not be able to access it. One workaround to this is to replace you ENTRYPOINT with a `sleep infinity` command of some sort. This way, the container will start but then immediately go to sleep indefinitely and will not encounter an error. You can then shell into the container and manually run your code to examine any errors that may occur.
