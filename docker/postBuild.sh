#!/usr/bin/env bash

jupyter contrib nbextension install --user
jupyter nbextension install --py --user latex_envs
jupyter nbextension enable --py widgetsnbextension
jupyter nbextension enable python-markdown/main
jupyter nbextension enable toc2/main
jupyter nbextension enable init_cell/main
jupyter nbextension enable --py latex_envs
