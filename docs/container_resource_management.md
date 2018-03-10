# Container Resource Management


When you specify a Pod, you can optionally specify how much CPU and memory (RAM) each Container needs. When Containers have resource requests specified, the scheduler can make better decisions about which nodes to place Pods on. And when Containers have their limits specified, contention for resources on a node can be handled in a specified manner. For more details about the difference between requests and limits, see Resource QoS.

[](https://medium.com/retailmenot-engineering/what-happens-when-a-kubernetes-pod-uses-too-much-memory-or-too-much-cpu-82165022f489)
