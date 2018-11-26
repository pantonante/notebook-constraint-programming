# Docker image for Constraint Programming (CPs)

## Prerequisites

- Docker 1.9.0+
- Docker-compose (or make 3.81+)

## Quickstart

Run `docker-compose up` and connect to the container! :clap:

## Need more Python packages?

Edit `requirements.txt` aadding any additional package you need.

## Post build configuration

The bash script `postBuild.sh` is executed at the end of the build process. It is useful to enable notebook extensions.

## iMiniZinc

[iMiniZinc](https://github.com/MiniZinc/iminizinc) module provides a cell magic extension for IPython/Jupyter notebooks and it's already configured to work on your notebook.

## Makefile

You can also use the makefile to build, run and stop the container

1. Run `make image` to create the image
2. Run `make run` to run and connect to the container
3. Run `make stop` to stop the server

## Authors

- [Pasquale Antonante](mailto:antonap@mit.edu)
- [Parker Lusk](https://github.com/plusk01)

## License

[MIT](LICENSE)
