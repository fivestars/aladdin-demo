# Autoscaling
Kubernetes provides autoscaling by CPU usage through a [HorizontalPodAutoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/). We give a simple demonstration of it in this demo project.

In order to enable autoscaling, the first step is to make sure that Heapster is enabled. We should have it deployed in all non-local environments, but if you are running this locally with minikube, you will need to manually enable it with

    $ minikube addons enable heapster

Next, we need to request cpu resources in the deployment file of the pod we are autoscaling. For each container in [aladdin-demo.deploy.yaml](../helm/aladdin-demo/templates/aladdin-demo.deploy.yaml), we add

    resources:
      requests:
        cpu: 100m
        
This is an optional field when not worrying about autoscaling, but it is required in order for the autoscaler to monitor percentage of cpu usage. In this example, we request 100 millicpu for each container. You can read more about what cpu means and how to manage other resources [here](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/). 

Next, we create the HorizontalPodAutoscaler object in [aladdin-demo.hpa.yaml](../helm/aladdin-demo/templates/aladdin-demo.hpa.yaml).

    apiVersion: autoscaling/v1
    # This is an autoscaler for aladdin-demo
    kind: HorizontalPodAutoscaler
    metadata:
      name: {{ .Chart.Name }}-hpa
      labels:
        project: {{ .Chart.Name }}
        name: {{ .Chart.Name }}-hpa
        app: {{ .Chart.Name }}-hpa
        githash: {{.Values.deploy.imageTag}}
    spec:
      scaleTargetRef:
        apiVersion: apps/v1beta1
        kind: Deployment
        name: {{ .Chart.Name }}
      minReplicas: 1
      maxReplicas: 10
      targetCPUUtilizationPercentage: 50

If the cpu utilization percentage of a pod exceeds 50%, the autoscaler will spin up new pods until each pod has a below 50% cpu utilization. This utilization percentage is quite low for purposes of demonstration. By default, autoscaler will check on the pods every 30 seconds. This can be changed through the controller manager's `--horizontal-pod-autoscaler-sync-period` flag.

We also add a `BusyResource` in [run.py](../app/run.py), which performs a CPU intensive operation upon get request to force autoscaling.

    class BusyResource(object):
        def on_get(self, req, resp):
            n = 0.0001
            for i in range(1000000):
                n += sqrt(n)
            resp.body = ('busy busy...')

    app = falcon.API()
    app.add_route('app/busy', BusyResource())

Confirm that the aladdin-demo app is running. Then check the status of the autoscaler and the current number of pods with

    $ kubectl get hpa
    NAME               REFERENCE                 TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
    aladdin-demo-hpa   Deployment/aladdin-demo   0% / 50%   1         10        1          51m
    
    $ kubectl get deployments
    NAME                 DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
    aladdin-demo         1         1         1            1           51m
    aladdin-demo-redis   1         1         1            1           51m
    
As expected, the CPU usage is well below the target 50%, so only one pod is needed.

Now we can manually increase the load by generating an infinite number of requests to the aladdin-demo service. Get the url of the aladdin demo with
    
    $ minikube service --url aladdin-demo
    <a url that looks something like http://192.168.99.100:30456>

Then, in a new terminal window, run
    
    $ kubectl run -i --tty load-generator --image=busybox /bin/sh

    Hit enter for command prompt

    $ while true; do wget -q -O- <url from previous step>/app/busy; done

This should return `busy busy...` ad infinitum. Let it run for about half a minute, since the autoscaler only checks on the pod every 30 seconds, and then look at the status of the autoscaler and pods again.

    $ kubectl get hpa
    NAME               REFERENCE                 TARGETS      MINPODS   MAXPODS   REPLICAS   AGE
    aladdin-demo-hpa   Deployment/aladdin-demo   182% / 50%   1         10        1          51m
    
    $ kubectl get deployments
    NAME                 DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
    aladdin-demo         4         4         4            4           51m
    aladdin-demo-redis   1         1         1            1           51m
    
We see now that the CPU usage is much higher than the target, and as a result the autoscaler has scaled the number of desired pods up to 4 to balance the load. Hooray!

Stop the inifinite query with `ctl c` and wait for a bit. You should see the CPU drop back down and the number of pods scaled back to 1. 
