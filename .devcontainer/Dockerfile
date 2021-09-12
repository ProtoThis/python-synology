FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.9

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# install test requirements
RUN python -m pip install \
        black \
        nox \
        nox-poetry \
        poetry \
        pylint

WORKDIR /workspaces

# Set the default shell to bash instead of sh
ENV SHELL /bin/bash
