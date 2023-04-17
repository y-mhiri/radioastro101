# Use the official Ubuntu 20.04 base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary dependencies
RUN apt-get update && apt-get install -y \
 python3.8 \
 python3-pip \
 software-properties-common \
 git

# Add KERN Suite repository and install python3-casacore
# RUN add-apt-repository -s ppa:kernsuite/kern-8 && \
#  apt-add-repository multiverse && \
#  apt-add-repository restricted && \
#  apt-get update && \
#  apt-get install -y python3-casacore

EXPOSE 8050
# Copy source code of the webapp
COPY . /opt/radioastro101

# Set the working directory
WORKDIR /opt/radioastro101

# RUN pip3 install .
RUN pip3 install .

# Set up an entrypoint to run the robii command when starting the container

CMD ["/opt/radioastro101/radioastro101/dash_app/app.py"]
ENTRYPOINT ["python3"]