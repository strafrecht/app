FROM gitpod/workspace-full

# Install custom tools, runtime, etc.
RUN sudo apt-get update     && sudo apt-get install -y         ...     && sudo rm -rf /var/lib/apt/lists/*

RUN sudo add-apt-repository ppa:ubuntugis/ppa

RUN sudo add-get update

RUN sudo apt-get install gdal-bin