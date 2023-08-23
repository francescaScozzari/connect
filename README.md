# Connect Orchestrator

This is the "Connect" orchestrator.

## Index

- [Quickstart](#quickstart)
  - [Git](#git)
    - [Clone](#clone)
  - [Environment variables](#environment-variables)
  - [Docker](#docker)
    - [Build](#build)
    - [Run](#run)
  - [Makefile shortcuts](#makefile-shortcuts)
    - [Pull](#pull)
    - [Django manage command](#django-manage-command)
    - [Restart and build services](#restart-and-build-services)
  - [Create SSL Certificate <sup id="a-setup-https-locally">1</sup>](#create-ssl-certificate-sup-ida-setup-https-locally1sup)
  - [Create and activate a local SSL Certificate <sup id="a-setup-https-locally">1</sup>](#create-and-activate-a-local-ssl-certificate-sup-ida-setup-https-locally1sup)
    - [Install the cert utils](#install-the-cert-utils)
    - [Import certificates](#import-certificates)
    - [Trust the self-signed server certificate](#trust-the-self-signed-server-certificate)

## Quickstart

This section explains the steps you need to clone and work with this project.

1. [clone](#clone) the project code
2. set all the required [environment variables](#environment-variables)
3. [build](#build) all the services
4. [create a superuser](#create-a-superuser) to login the platform
5. [run](#run) all the services
6. login using the URL: http://localhost:8080

### Git

#### Clone

Clone the orchestrator and services repositories:

```console
git clone git@gitlab.com:uda-connect/orchestrator.git connect
cd connect
git clone -b mian git@gitlab.com:uda-connect/backend.git
git clone -b mian git@gitlab.com:uda-connect/frontend.git
cd ..
```

**NOTE** : We're cloning the `main` branch for all repo.

### Environment variables

In order for the project to run correctly, a number of environment variables must be set in an `.env` file inside the orchestrator directory. For ease of use, a `.env_template` template is provided.

Enter the newly created **project** directory and create the `.env` file copying from `.env_template`:

```console
$ cd ~/projects/connect
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

**NOTE**: It can be daemonized adding the `-d` flag.

### Makefile shortcuts

#### Self documentation of Makefile commands

To show the Makefile self documentation help:

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

Import the `traefik/conf/local/unsigned.crt` file in your browser to have a trusted ssl certificate:

#### Firefox

- Settings > Privacy & Security > Manage Certificates > View Certificates... > Authorities > Import

#### Chrome

- Settings > Security > Certificates > Authorities > Import
