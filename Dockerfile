################################################
# Dockerfile to build panyabot container images
# Based on raspbian
################################################
#Set the base image to raspbian
FROM resin/raspberrypi-systemd:wheezy

# File Author / Maintainer
MAINTAINER Wachira Ndaiga

# Expose ports
EXPOSE 5000

# Create environment variables
ENV INITSYSTEM on
ENV XDG_RUNTIME_DIR /run/user/%I

# Update the repository sources list and install dependancies
RUN sudo apt-get update \
  && apt-get install -y \
    python \
    python-dev \
    python-pip \
    usbutils \
    bluez \
    python-gobject \
    python-bluez \
    nano \
    arduino-mk \
    wget \
    ca-certificates \
    picocom \
    make \
  && apt-get clean

# Set application directory
RUN mkdir /webot
WORKDIR /webot

# we install requirements first to benefit from docker layers caching
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# copy the entire source code
ADD . ./

# set permissions
RUN chmod 755 db_start.py tests.py run.py run.sh app/hostcon.sh firmwareman.sh

# Start the web app
CMD ["/bin/bash", "run.sh"]