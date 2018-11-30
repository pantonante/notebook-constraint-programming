#------------------------------------------------------------------------------#
# This file contains the setup for building a Jupyter Notebook image with 
# MiniZinc support. It uses multi-stage builds in order to keep the images small.
# Note that the statements ADD, RUN, and COPY can add image layers.
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# Setup MiniZinc base image

FROM alpine:latest AS builder

# Retrieve MiniZinc IDE distribution
ADD https://github.com/MiniZinc/MiniZincIDE/releases/download/2.2.3/MiniZincIDE-2.2.3-bundle-linux-x86_64.tgz /minizinc.tgz

# Unpack compressed MiniZinc archive and renamed folder
RUN tar -zxf /minizinc.tgz && \
    mv /MiniZincIDE-2.2.3-bundle-linux /minizinc

#------------------------------------------------------------------------------#
# Extend Jypiter Notebook image
# Get image
FROM jupyter/base-notebook:a6fc0cfbd01b

# Switch back to root
USER root

# Update Ubuntu and install necessary packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libharfbuzz0b \
    libpcre16-3 \
    libgl1-mesa-glx \
    libgeos-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Copy unpacked MiniZinc installation from the build image
COPY --from=builder /minizinc /minizinc
RUN fix-permissions /minizinc

#------------------------------------------------------------------------------#
# Additional Python packages Variables
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Setup Jupyter extensions
ADD postBuild.sh /tmp/
RUN /bin/sh /tmp/postBuild.sh
RUN fix-permissions /home/$NB_USER

#------------------------------------------------------------------------------#
# Cleaning up packages
RUN apt-get purge -y build-essential &&\
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#------------------------------------------------------------------------------#
# Removing work directory
RUN rm -rf /home/jovyan/work

#------------------------------------------------------------------------------#
# Environment Variables
# Switch back to jovyan to avoid accidental container runs as root
USER $NB_USER

# Add MiniZinc's binary path to PATH
ENV PATH="/minizinc:/minizinc/bin:${PATH}"

# Add MiniZinc's library path to LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH="/minizinc/lib:${LD_LIBRARY_PATH}"
