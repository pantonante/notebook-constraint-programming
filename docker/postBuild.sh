#!/usr/bin/env bash

jupyter contrib nbextension install --user
jupyter nbextension enable --py widgetsnbextension
jupyter nbextension enable python-markdown/main
