FROM osrf/ros:galactic-desktop

SHELL ["/bin/bash", "-c"]

RUN apt-get update
RUN apt install python-setuptools -y
### Required to install python packages
#RUN apt-get install python3 python3-pip -y
# Install system packages

COPY . /ros2_ws
WORKDIR /ros2_ws

RUN bash  test.sh
