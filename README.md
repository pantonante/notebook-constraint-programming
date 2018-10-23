# 16.413 Project

## Install

The easiest way to use this repository is to use `repo2docker`, if you choose to not use skip this section.

### Prerequisites

1. Docker to build & run the repositories. The [community edition](https://store.docker.com/search?type=edition&offering=community)
   is recommended.
2. Python 3.4+.

### Install repo2docker

It is raccomended to install it from source since the pip package is missing of some features:

```bash
git clone https://github.com/jupyter/repo2docker.git
cd repo2docker
pip install -e .
```

## Crete Docker container

To create the Docker container clone this repository in a folder of your choice, than run

```bash
repo2docker -E project-16.413/.
```

Than connect to the running container. Note that the flag `-E` set up the editable mode so what you change in the Jupyter notebook is reflected in the local folder.
