FROM ubuntu:latest
MAINTAINER wildduck.io

# provision the image
RUN apt-get update -y
RUN apt-get install -y python-dev build-essential python3 python3-pip

ADD requirements.txt /opt/server/requirements.txt
RUN pip3 install -r /opt/server/requirements.txt

# Add the wait-for-it script so docker-compose can ensure depenency containers come up first
ADD wait-for-it/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
