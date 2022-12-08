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

## Best Practices For Application Deployment
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

## Docker for Application Packaging
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

