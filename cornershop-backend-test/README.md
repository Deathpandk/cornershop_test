## cornershop-backend-test

## App description

To access Nora's panel go to http://127.0.0.1:8000 and login with a created user.

In "employees" tab you can create and see registered employees, 
when creating a new employee, make sure to use a valid slack_id,
app validates slack_id by sending a welcome message.

In "menus" tab you can create new menus for any date and add options to them,
also you can see every order made for a certain menu.

The Option-Adding form is shared between different menus.

When clicking "send slack messages" app will send reminders to
all registered employees with their own uuid to make an order.

In /menu/uuid/ employees can make an order for the current day's menu before 11am.

** Some handy features (as update and delete objects) are not available, sorry for that :(.

## Commands

### Configure Slack

* Enter Slack Test workspace to use Nora's App:
https://join.slack.com/t/slacktestred/shared_invite/zt-1dz9ffw1v-7tQ9wEoAxiVx6KolHPwfxw
* In channel #general you'll find Nora slack token, on `docker-compose` please set
env variable SLACK_TOKEN= with the current token
* You can find example slack id's in Slack Test #general channel for testing purposes

### Running the development environment

* `make up`
* `dev up`
* `dev createsuperuser` (needed for administration panel)

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000


### About building local environment with Linux systems

If you bring up the local environment in a linux system, maybe you can get some problems about users permissions when working with Docker.
So we give you a little procedure to avoid problems with users permissions structure in Linux.:

1- Delete containers

```
# or docker rm -f $(docker ps -aq) if you don't use docker beyond the test
make down
```

2- Give permissions to your system users to use Docker

```
## Where ${USER} is your current user
sudo usermod -aG docker ${USER}
```

3- Confirm current user is in docker group

```
## If you don't see docker in the list, then you possibly need to log off and log in again in your computer.
id -nG
```


4-  Get the current user id

```
## Commonly your user id number is near to 1000
id -u
```

5- Replace user id in Dockerfiles by your current user id

Edit `.docker/Dockerfile_base` and replace 1337 by your user id.

6- Rebuild the local environment 

```
make rebuild
make up
```