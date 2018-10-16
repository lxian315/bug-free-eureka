# Docker

A Docker Compose Service with no build configuration.

Docker Compose Service works on macOS, Windows, and Linux. [Creating a service](https://docs.docker.com/compose/) – How to create a new service.

## Quick Overview
* Install [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and [Docker Compose](https://docs.docker.com/compose/install/) if you haven't already.
* Go into the project's directory (should contain the [docker-compose.yml](https://docs.docker.com/compose/compose-file/) file) and build the images

```sh
docker-compose up --build -d
```

*You only need to run this command once to build the images. Docker is smart enough to pickup changes in your code base.*

* After you successfully build your images, you'll need to go inside the Django container to sync with the database. You can do this with the following commands


```sh
docker exec -it <<container>> bash  #Here container is bug-free-eureka-master_web_1
python manage.py makemigrations
python manage.py migrate
```

*CTR D to exit the container*

* To stop the service, simply run

```sh
docker-compose stop
```

* Now that your images are built, you can start your service again with

```sh
docker-compose up
```

*Important: this command should only be run after your images are built.*
