#!/bin/bash
apt-get update -y
apt-get install docker.io -y
apt-get install docker-compose -y
git clone https://github.com/ansaldimatteo/simple-flask-app.git
cd simple-flask-app/
docker-compose up -d