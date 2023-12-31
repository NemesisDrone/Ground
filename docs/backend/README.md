# Backend documentation

Here is some nice documentations to read : 
- [Django](https://docs.djangoproject.com/en/4.2/)
- [Django Channels](https://channels.readthedocs.io/en/stable/)(used for websocket)
- [Django Rest Framework](https://www.django-rest-framework.org/) (not used yet, but still interesting to read)
- [How JWT works](https://sureshdsk.dev/how-json-web-token-jwt-authentication-works/) (used for authentication)

## Apps
Our django project is composed of 3 apps:
- `core` which contains utilities, models and function that are reused in the other apps.
- `user` which contains the user model and the authentication system as well as the user profile.
- `communication` which contains the communication using websocket with the frontend/interfaces to the drone.

## Docker
The backend is running inside a docker container.
The docker compose file start a postgres database, a redis server and the backend.
To start the backend, you need to be in the root folder of the project.
```bash
docker-compose up
```

When you add a python dependency, you need to rebuild the docker image:
```bash
docker-compose up --build
```

You will need to run migrations or access the python/django shell. To do so, you need to run the following command to go inside the container:
```bash
docker-compose exec backend /bin/bash
# and then you can run any commands you want
python manage.py migrate
python manage.py shell_plus
...
```
