# Nemesis Ground Station
In this repository, you can find the frontend, the backend, and the communication between the Drone and the station.


## Frontend
The frontend is made with Vuejs 3 with Nuxt and Typescript.
The frontend is located in the `frontend` folder.

### Setup
Make sure to install the dependencies:

```bash
# /frontend
yarn install
```

### Development 
To start developing the frontend, run the following command:

```bash
# /frontend
yarn dev
```

[Frontend documentation](frontend/README.md)

## Backend
The backend is made with Python using Django and running inside a Docker container.
The backend code is located in the `backend` folder.

### Development
To start developing the backend, run the following command:
You need to be in the root folder of the project.
```bash
docker-compose up
```

When you add a python dependency, you need to rebuild the docker image:
```bash
docker-compose up --build
```
[Backend documentation](backend/README.md)
