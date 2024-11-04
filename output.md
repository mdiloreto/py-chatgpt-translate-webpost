# Kubernetes networking – Part 2


In the first part of this series of Posts, we were doing a basic explanation of how Networking works in Kubernetes.

In this second part of the Kubernetes Networking Blog Posts series, we'll be exploring the typical networking models in various Kubernetes implementations.
![Image](https://madsblog.net/wp-content/uploads/2024/10/Portada.jpg)

## Typical Kubernetes Networking Models


There are different variants of the implementation of the Networking Model in Kubernetes. Any of these implementations must have the following characteristics:

* Each Pod must have a unique IP across the cluster. 
* Pods must communicate with other Pods on all nodes without using NAT. 
* Kubelet must be able to communicate with all Pods on the node.




There are 3 types of implementations:

* Fully integrated model (flat).
* Bridge Model (Island).
* Air-gapped model




These 3 implementations vary in:

* As pods communicate with services outside of Kubernetes on the corporate network. 
* As pods communicate with other clusters in the organization. 
* If NAT is required for outbound-to-external communication. 
* If the IPs of the Pods can be reused in another cluster of the corporate network. 




As you may have noticed, each of the Cloud Providres can implement one or more of these models, giving several deployment options.
## Fully integrated model (flat).

![Image](https://madsblog.net/wp-content/uploads/2024/10/image-1.png)


One of the main advantages of this model is that Cloud Providers can tightly integrate Kubernetes deployment with Software-Defined Networks (SDNs).

The key to the operation of this model is that the IP addresses of the pods are routed within the network where the Cluster is located. The underlying network knows which node the pods are on. This can be handled by Routes in GCP or Effective Routes in Azure.

Some deployments use an isolated, separate CIDR for pods, but it's not a mandatory condition. In some implementations, the Pods take the ips from the same network where the Cluster is located.

In this deployment, pods do not need NAT to communicate with other applications outside the cluster.
## Deployment in different Cloud Providers:


* GKE uses this model with VPC-native Clusters. Services and Pods ranges are assigned as secondary ranges of the nodes' VPC. For external traffic, SNAT can be used to map the IP of the Pod to that of the node. 
* AKS uses this model in Azure CNI and Azure CNI dynamic configurations. In Azure CNI, IPs from the same network as the Clusters are used and in Dynamic we can assign a separate Subnet in the VNET for this purpose, allowing different NSG implementations.
* EKS uses this model when using the Amazon VPC Container Networking interface (CNI) Plugin. Allows you to assign IPs to pods directly from an address space in a VPC. This subnet can be the one where the nodes are located or a dedicated subnet. Similar to the variation in AKS.  



## Advantages:


* Better telemetry and debugging. 
* Makes it easy to configure Firewall rules.
* Better compatibility.
* Service Mesh Support 



## Disadvantages:


* Extensive use of IP addresses as large quantities will be needed for pods.  
* SDN requirements: Requires very deep integration with the underlying network. Difficult to implement in Self-Managed/On-premises.



## Bridge Model (Island)

![Image](https://madsblog.net/wp-content/uploads/2024/10/image-2-1024x925.png)


This model is commonly used On-Premises where it is not possible to make a tight integration with the underlying network. With this model, Pods can communicate with resources outside the cluster through a Gateway or Proxy. Pods within the Cluster can communicate freely.

For the implementation of Proxys/Gateways there are different deployment models:

* Use Nodes as Gateways: SNAT is used for Outbound. For communication to the Services, the Services such as NodePort or LoadBalancer can be used. 
* Use Proxy VMs: VMs must have two NICs, one in the network of the nodes and the other in the Enterprise Network. 



## Deployment in different Cloud Providers:


* GKE and EKS do not use this model. 
* By default AKS uses this model when using Kubenet, UDRs are used for Pod-to-Pod traffic with Ip Forwarding at the level of the node NICs. For outbound traffic, SNAT is used. 



## Advantages:


* CIDRs can be reused in other clusters, although it is a bit risky for external communication. It should be carefully planned and equally recommended to reserve a single network-wide range for pods and use this range for all clusters. 
* Easier security: since the pods are not exposed to the rest of the network. 



## Disadvantages:


* Inaccurate telemetry and difficult debugging: traffic is only recorded with the IP of the Nodes. 
* More difficult to configure firewalls: only the IP of the nodes can be used. 
* Service Meshes incompatibility.



## Air-gapped model

![Image](https://madsblog.net/wp-content/uploads/2024/10/image-3.png)


This model is mostly used for Clousters who do not need access to the corporate network. Only through Public APIs. In this model, the cluster cannot communicate with other resources using private IPs. Pods within the cluster can communicate freely.

This model is not commonly used but an isolated network can be achieved in any deployment. You only need to deploy the cluster on a separate network with no connectivity to other services on the corporate network.
## Advantages:


* All internal ranks can be reused. 
* Safety by total isolation. 



## Disadvantages:


* No private communication.




Mateo Di Loreto
