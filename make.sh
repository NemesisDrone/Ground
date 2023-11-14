#!/bin/bash

set -e # Exit script if a execution fail

# Install node dependcies on debian/ubuntu based system
if ! type "yarn" > /dev/null; then
        echo "Yarn is not installed..."
        sudo apt update -y
        sudo apt install nodejs npm -y
        sudo npm install -g yarn
        echo "Done !"
fi

# Check Docker installation...
if ! type "docker" > /dev/null; then
        echo "Docker is not installed..."
        sudo apt update -y
        sudo apt install docker.io docker-compose -y
        echo "Done !"
fi

if ! type "docker-compose" > /dev/null; then
        echo "Docker-compose is not installed..."
        sudo apt update -y
        sudo apt install docker-compose -y
        echo "Done !"
fi

# Check if the file is executing in the right folder.
if [ ! -e "docker-compose.yml" ]
then
    echo "ERROR: Please run this file at the root of the project."
    exit 1
fi

sudo docker network create ground_network || true
sudo docker-compose up &
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python populatedb.py
cd frontend
yarn install

# Check Docker installation...
if ! type "lolcat" > /dev/null; then
        echo "Lolcat is not installed..."
        sudo apt update -y
        sudo apt install lolcat -y
        echo "Done !"
fi

echo "                                                                
                                                                
    /|    / /                                                   
   //|   / /  ___      _   __      ___      ___     ( )  ___    
  // |  / / //___) ) // ) )  ) ) //___) ) ((   ) ) / / ((   ) ) 
 //  | / / //       // / /  / / //         \ \    / /   \ \     
//   |/ / ((____   // / /  / / ((____   //   ) ) / / //   ) )   
" | lolcat

echo "cd frontend and run yarn dev to start coding !!!"
exit 0
