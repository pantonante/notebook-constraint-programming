# Interactive tutorial on Constraint Programming (CPs)

This repository contains a jupyter notebook with an in-depth tutorial on constraint programming. To show the overall mechanics of constraint programmin the code contains model coded in MiniZinc, Google OR-Tools and custom n-Queens solver.

Please use the docker container to enable all the functionalities.

## Prerequisites

- Docker 1.9.0+
- Docker-compose **or** make 3.81+

## Quickstart

### Using Docker-compose

Run `docker-compose up` and connect to the container! :clap:

### Using Makefile

You can also use the makefile to build, run and stop the container

1. Run `make image` to create the image
2. Run `make run` to run and connect to the container
3. Run `make stop` to stop the server
   
## Extend the Docker container

### Need more Python packages?

Edit `requirements.txt` aadding any additional package you need.

### Post build configuration

The bash script `postBuild.sh` is executed at the end of the build process. It is useful to enable notebook extensions.

## Authors

- [Pasquale Antonante](mailto:antonap@mit.edu)
- [Parker Lusk](https://github.com/plusk01)

## License

[MIT](LICENSE)
