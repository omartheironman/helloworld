# Overview

This repo contains a simple application called helloworld. All it does is respond to an http request with "hello world!", the application is written using 
fastAPI to be able to integrate swagger and schema definitions. 

# Automation

*** Terragrunt is used to configure terraform modules and store backend 
*** Github Actions will execute:
    1- Unit test
    2- Build and Pubsish docker file
    3- Deploy infrastructure change
    4- Deploy the application using helm



# High level Architecture 
<img width="828" alt="image" src="https://user-images.githubusercontent.com/58672497/234667857-bb01d374-7689-4001-a70b-44a45039ed26.png">

There are 3 main cluster located in USA, Asia and Europe. The helm chart is configured to support HPA incase of highload. I could have added redis and prometheus
but I couldn't get a response in time so I just proceeded forward with my current design. 

1- A client sends a request to access a particular application or service hosted on the GCP cluster.

2- The request first reaches the load balancer that is set up with an ingress class of gce.

3- The load balancer checks its configuration to determine which backend service should handle the request. In this case, the backend service is configured as nodetype port, which means that the traffic will be forwarded to a Kubernetes Service with a type of NodePort.

4- The load balancer then forwards the request to the Kubernetes Service, which acts as a virtual IP for the pods running the application.

5- The Kubernetes Service checks its configuration to determine which backend pod should handle the request. 

6- The service forwards the request to the pod that is currently serving the application.

7- when the Kubernetes Service receives the request from the load balancer, kube-proxy running on the node where the pod is running intercepts the request. Kube-proxy then routes the request to the appropriate pod based on the pod's IP address and the service's port number.

8- The pod processes the request and sends a response back to the Kubernetes Service.

9- The Kubernetes Service sends the response back to the load balancer.

10- The load balancer forwards the response back to the client that initiated the request.
