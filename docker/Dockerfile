#------------------------------------------------------------------------------#
# This file contains the setup for building a Jupyter Notebook image with 
# MiniZinc support. It uses multi-stage builds in order to keep the images small.
# Note that the statements ADD, RUN, and COPY can add image layers.
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# Setup MiniZinc base image

ARG BASE_CONTAINER=ubuntu:bionic-20180526@sha256:c8c275751219dadad8fa56b3ac41ca6cb22219ff117ca98fe82b42f24e1ba64e
FROM $BASE_CONTAINER AS builder

# Retrieve MiniZinc IDE distribution
ADD https://github.com/MiniZinc/MiniZincIDE/releases/download/2.2.3/MiniZincIDE-2.2.3-bundle-linux.tgz /minizinc.tgz

# Unpack compressed MiniZinc archive and renamed folder
RUN tar -zxf /minizinc.tgz && \
    mv /MiniZincIDE-2.2.3-bundle-linux /minizinc

#------------------------------------------------------------------------------#
# Extend Jypiter Notebook image

# Get image
FROM jupyter/minimal-notebook:610bb8b938db

# Switch back to root
USER root

# Update Ubuntu and install necessary packages
RUN apt-get update -y && apt-get install -y \
    vim \
    libharfbuzz0b \
    libpcre16-3 \
    libgl1-mesa-glx

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
# Environment Variables
# Switch back to jovyan to avoid accidental container runs as root
USER $NB_USER

# Add FlatZinc solver absolute path
ENV FZNEXEC="/entry_data/fzn-exec"

# Add MiniZinc's binary path to PATH
ENV PATH="/minizinc:/minizinc/bin:${PATH}"

# Add MiniZinc's library path to LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH="/minizinc/lib:${LD_LIBRARY_PATH}"
