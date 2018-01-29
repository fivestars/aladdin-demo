# Jobs and Cronjobs

A job in Kubernetes essentially ensures that a something is run to completion by monitoring the success of pods and creating new ones if necessary. It is generally used to supervise pods that run batch processes taking some amount of time to complete, for example a calculation or back up operation. From the [Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/):

> A job creates one or more pods and ensures that a specified number of them successfully terminate. As pods successfully complete, the job tracks the successful completions. When a specified number of successful completions is reached, the job itself is complete. Deleting a Job will cleanup the pods it created.

> A simple case is to create one Job object in order to reliably run one Pod to completion. The Job object will start a new Pod if the first pod fails or is deleted (for example due to a node hardware failure or a node reboot).

> A Job can also be used to run multiple pods in parallel.




