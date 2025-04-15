# Connect Orchestrator

This is the orchestrator for the "Connect" web app.

A "self-explainable" AI platform (Connect),
an open cloud platform based on explainable artificial intelligence (XAI) for matching research interests.

## Index

- [Remote setup](#remote-setup)
  - [Git clone](#git-clone-remote)
  - [Environment variables](#environment-variables-remote)
  - [Automated deployment](#automated-deployment)
  - [Manual deployment](#manual-deployment)
  - [Run with docker compose](#run-with-docker-compose)
  - [Populate data](#populate-data)
- [Local setup](#local-setup)
  - [Git clone](#git-clone)
  - [Environment variables](#environment-variables)
  - [Docker](#docker)
    - [Build](#build)
    - [Run](#run)
  - [Makefile shortcuts](#makefile-shortcuts)
    - [Pull](#pull)
    - [Django manage command](#django-manage-command)
    - [Restart and build services](#restart-and-build-services)
  - [Activate a valid local SSL Certificate](#activate-a-valid-local-ssl-certificate)

## Remote setup

This section explains the steps you need to set up the project remote execution.

### Git clone (remote)

Clone the orchestrator and services repositories:

```console
$ git clone git@gitlab.com:uda-connect/orchestrator.git connect
$ cd connect
```

### Environment variables (remote)

For the project to run correctly, some environment variables must be set in a `.env` file inside the orchestrator directory. For ease of use, a `.env_template` template is provided.

Enter the newly created **project** directory and create the `.env` file copying from `.env_template`:

```console
$ cd ~/connect
$ cp .env_template .env
```

Ensure that all environment variables are properly configured and that the `COMPOSE_FILE` variable in the `.env` file is set as shown below:

```ini
COMPOSE_FILE=docker-compose.yaml:./docker-compose/remote.yaml
```

### Automated deployment

Configure the backend and frontend services pipeline to support automated deployments.

[https://docs.gitlab.com/ee/ci/ssh_keys/](https://docs.gitlab.com/ee/ci/ssh_keys/)

### Manual deployment

Retrieve all the latest released images from the container registry.

```console
$ docker login registry.gitlab.com
$ docker pull registry.gitlab.com/uda-connect/backend:v.0.0.0
$ docker pull registry.gitlab.com/uda-connect/frontend:v.0.0.0
$ docker logout
```

Export the environment variables with the latest released image versions for each service, for example:

```console
$ export BACKEND_IMAGE=registry.gitlab.com/uda-connect/backend:v.0.0.0
$ export FRONTEND_IMAGE=registry.gitlab.com/uda-connect/frontend:v.0.0.0
```

### Run with docker compose

```console
$ docker compose up -d
```

### Populate data

#### Import authors

Before importing authors into a relational database, copy your `.txt` files with author IDs into `./data` directory.

```console
$ mkdir -p .cache
$ ./scripts/import_authors.sh ./data/<author_ids_file>.txt
```

**Note**: The `import_authors` process generates a cache stored in the `~/.cache` directory
(if not exist create it with the right user permissions before script execution).

#### Load documents

To load documents to vector database

```console
$ ./scripts/load_documents.sh
```

If you wish to limit the number of documents to be processed (e.g., from 0 to 100)

```console
$ ./scripts/load_documents.sh 0 100
```

## Local setup

This section explains the steps you need to clone and work with this project.

1. [Git clone](#git-clone) the project code
2. set all the required [environment variables](#environment-variables)
3. [build](#build) all the services
4. [create a superuser](#create-a-superuser) to log in to the platform
5. [run](#run) all the services
6. login using the URL: http://localhost:8080

### Git clone

Clone the orchestrator and services repositories:

```console
$ git clone git@gitlab.com:uda-connect/orchestrator.git connect
$ cd connect
$ git clone -b main git@gitlab.com:uda-connect/backend.git
$ git clone -b main git@gitlab.com:uda-connect/frontend.git
$ cd ..
```

**NOTE**: We're cloning the `main` branch for all repositories.

### Environment variables

For the project to run correctly, some environment variables must be set in a `.env` file inside the orchestrator directory. For ease of use, a `.env_template` template is provided.

Enter the newly created **project** directory and create the `.env` file copying from `.env_template`:

```console
$ cd ~/connect
$ cp .env_template .env
```

### Docker

All the following Docker commands are supposed to be run from the orchestrator directory.

#### Build

```console
$ docker-compose build
```

#### Run

```console
$ docker-compose up
```

**NOTE**: It can be daemonized by adding the `-d` flag.

### Makefile shortcuts

#### Self-documentation of Makefile commands

To show the Makefile self-documentation help:

```console
$ make
```

#### Pull

Pull the main git repo and the sub-repos:

```console
$ make pull
```

#### Django manage command

Use the Django `manage.py` command shell:

```console
$ make django
```

You can pass the specific command:

```console
$ make django p=check
```

You can pass the container name:

```console
$ make django p=shell c=backend_2
```

#### Restart and build services

Restart and build all services:

```console
$ make rebuild
```

You can pass the service name:

```console
$ make rebuild s=backend
```

### Activate a valid local SSL Certificate

Import the `traefik/conf/local/unsigned.crt` file in your browser to have a trusted SSL certificate:

#### Firefox

- Settings > Privacy & Security > Manage Certificates > View Certificates... > Authorities > Import

#### Chrome

- Settings > Security > Certificates > Authorities > Import
