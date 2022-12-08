# TechTrends

## Background
TechTrends is an online website used as a news sharing platform, that enables consumers to access the latest news within the cloud-native ecosystem. In addition to accessing the available articles, readers are able to create new media articles and share them.

Imagine the following scenario: you joined a small team as a Platform Engineer. The team is composed of 2 developers, 1 platform engineer (you), 1 project manager, and 1 manager. The team was assigned with the TechTrends project, aiming to build a fully functional online news sharing platform. The developers in the team are currently working on the first prototype of the TechTrends website. As a platform engineer, you should package and deploy TechTrends to Kubernetes using a CI/CD pipeline.

The web application is written using the Python Flask framework. It uses SQLite, a lightweight disk-based database to store the submitted articles.

Below you can examine the main components of the firsts prototype of the application:

About page - presents a quick overview of the TechTrends site
Index page - contains the content of the main page, with a list of all available posts within TechTrends
New Post page - provides a form to submit a new post
404 page - is rendered when an article ID does not exist is accessed

And lastly, the first prototype of the application is storing and accessing posts from the "POSTS" SQL table. A post entry contains the post ID (primary key), creation timestamp, title, and content.

### Project Steps Overview
Apply the best development practices and develop the status and health check endpoints for the TechTrends application.
Package the TechTrends application by creating a Dockerfile and Docker image.
Implement the Continuous Integration practices, by using GitHub Actions to automate the build and push of the Docker image to DockerHub.
Construct the Kubernetes declarative manifests to deploy TechTrends to a sandbox namespace within a Kubernetes cluster. The cluster should be provisioned using k3s in a vagrant box.
Template the Kubernetes manifests using a Helm chart and provide the input configuration files for staging and production environments.
Implement the Continuous Delivery practices, by deploying the TechTrends application to staging and production environments using ArgoCD and the Helm chart.

## 1. Best Practices For Application Deployment
The metrics and health check endpoints were added, in addition to logging functionality.

**Healthcheck endpoint**
The /healthz endpoint for the TechTrends application. 
The endpoint returns the following response:

An HTTP 200 status code
A JSON response containing the result: OK - healthy message

**Metrics endpoint**
A /metrics endpoint that returns the following:

An HTTP 200 status code
A JSON response with the following metrics:
Total amount of posts in the database
Total amount of connections to the database. For example, accessing an article will query the database, hence will count as a connection.
Example output: {"db_connection_count": 1, "post_count": 7}

**Logs**
The TechTrends application logs the following events:

An existing article is retrieved. The title of the article should be recorded in the log line.
A non-existing article is accessed and a 404 page is returned.
The "About Us" page is retrieved.
A new article is created. The title of the new article should be recorded in the logline.
Every log line should include the timestamp and be outputted to the STDOUT. Also, capture any Python logs at the DEBUG level.

## 2. Docker for Application Packaging
This step focuses on packaging the application using Docker. I wrote a Dockerfile and build a Docker image for the TechTrends project. I had the application running locally inside a Docker container.

### Dockerfile
A Dockerfile was built with instructions to package the TechTrends application. The Dockerfile should contain the following steps:

Use a Python base image in version 3.8
Expose the application port 3111
Install packages defined in the requirements.txt file
Ensure that the database is initialized with the pre-defined posts in the init_db.py file
The application should execute at the container start

### Docker Image
Using the Dockerfile defined above, create a Docker image and test it locally. The Docker build command should:

Reference the defined Dockerfile
Tag the image as techtrends
Make sure you specify the location of the Dockerfile
Note: Place the used Docker commands in the docker_commands file.

Run and test locally
Test the Docker image locally, with the following specifications:

Using the detached mode
Expose the application port on port 7111 on the host machine, e.g., use the -p 7111:3111 option.
Note: Place the Docker run in the docker_commands file.

Access the application in the browser using the http://127.0.0.1:7111 endpoint and try to click on some of the available posts, create a new post, access the metrics endpoint, etc.

## 3. Continuous Integration with GitHub Actions
This step uses the Continuous Integration (CI) fundamentals and automate the packaging of the TechTrends application. I used GitHub Actions to build, tag, and push the TechTrends Docker image to DockerHub. As a result, I have a functional GitHub Action that will construct a new image with every new commit to the main branch.

### GitHub Actions
I created a GitHub Action that will package and push the new image for the TechTrends application to DockerHub. The configuration file has the name techtrends-dockerhub.yml in the .github/workflows/ directory. If the directory does not exist, create it using the mkdir -p .github/workflows/ command.

These functionalities are implemented using the Build and Push Docker images upstream GitHub Action as the basis. The following action uses DockerHub Tokens and encrypted GitHub secrets to login into DockerHub and to push new images. To set up these credentials refer to the following resources:

Create DockerHub Tokens
Create GitHub encrypted secrets
Construct a GitHub Action, that would package and push the TechTrends application with the following requirements:

name - "TechTrends - Package with Docker"
Trigger on every push to the main branch
Run the action on the ubuntu-latest operating system
For the Docker build and push step:
Context should be set to the project directory.
Note that the context in the current Step 3 refers to GitHub Actions and has nothing to do with the context in the previous Step 2.

Reference the Dockerfile for TechTrends application
Push the image to DockerHub with the tag techtrends:latest
After creating the GitHub Action verify it executes successfully when a new commit is pushed to the master branch. Verify your DockerHub account for the TechTrends image with the tag latest being pushed successfully.

## 4. Kubernetes Declarative Manifests
In this step, I deploy a Kubernetes cluster using k3s and deploy the TechTrends application. I created declarative Kubernetes manifests and release the application to the sandbox environment. 

### Deploy a Kubernetes cluster
Using vagrant, create a Kubernetes cluster with k3s. Refer to the Vagrantfile from the repository. Make sure to have vagrant and VirtualBox 6.1.16 or higher installed.

To create a vagrant box and ssh into it, use the following commands:

vagrant up
vagrant ssh

To deploy the Kubernetes cluster, refer to the k3s documentation. Note: To interact with the cluster kubectl, you need to have root access to the kubeconfig file. Hence, use sudo su - to become root and use kubectl commands.

Verify if the cluster is operational by evaluating if the node in the cluster is up and running. You can use the kubectl get no command.

Note: Take a screenshot of the kubectl get no output, and place it in the screenshots folder with the name k8s-nodes.

Kubernetes Declarative Manifests
Using the declarative approach, deploy the TechTrends application to the Kubernetes cluster. Construct the YAML manifests for the following resources:

Namespace in namespace.yaml file:
  name: sandbox

Deployment in deploy.yaml file:
  namespace: sandbox
  image: techtrends:latest
  name:techtrends
  replicas: 1
  resources:
    requests: CPU 250m and memory 64Mi
    limits: CPU 500m and memory 128Mi
  container port: 3111
  liveness probe:
    path: /healthz
    port: 3111
  readiness probe:
    path: /healthz
    port: 3111
Service in service.yaml file:
  namespace: sandbox
  name: techtrends
  port: 4111
  target port: 3111
  protocol: TCP
  type: ClusterIP

### Deploy TechTrends with Kubernetes manifests
Using the Kubernetes manifests and kubectl commands, deploy the TechTrends application to the k3s cluster. As a result, you should have the following resource created:

a sandbox namespace
a techtrends deployment, in the sandbox namespace with 1 replica or pod running
a techtrends service that exposes the TechTrends application on port 4111 using a ClusterIP

