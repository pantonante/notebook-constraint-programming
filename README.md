This folder contains supporting material for 16.413 final project.

## Prerequisites

* make 3.81+
    * Ubuntu users: Be aware of [make 3.81 defect 483086](https://bugs.launchpad.net/ubuntu/+source/make-dfsg/+bug/483086) which exists in 14.04 LTS but is fixed in 15.04+
* docker 1.9.0+

## Quickstart

1. Run `make image` to create the image
2. Run `make run` to run and connect to the container
3. Run `make stop` to stop the server

## Need more Python packages?

Edit `requirements.txt` aadding any additional package you need.

## Post build configuration

The bash script `postBuild.sh` is executed at the end of the build process. It is useful to enable notebook extension.

## iMiniZinc

[iMiniZinc](https://github.com/MiniZinc/iminizinc) module provides a cell magic extension for IPython/Jupyter notebooks and it's already configured to work on your notebook.

## Uh ... make?

Yes, sorry Windows users.
