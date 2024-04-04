FROM python:3.12.2-slim-bookworm


ENV APP_USER=dev \
    DEBIAN_FRONTEND=noninteractive

# Create a dedicated user
RUN useradd -ms /bin/bash ${APP_USER}

RUN apt-get update
# tools for debug
RUN apt-get install -y --no-install-recommends \
    sudo curl iputils-ping iproute2 pipx

RUN usermod -aG sudo ${APP_USER}
RUN passwd --delete ${APP_USER}

USER ${APP_USER}

# we install virtual env only for the app user
RUN python3 -m venv ~/.venv

RUN echo ". ~/.venv/bin/activate" >> ~/.bashrc