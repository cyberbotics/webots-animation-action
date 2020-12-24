FROM cyberbotics/webots:latest

RUN apt-get update && \ 	
    apt-get install -y \
        git \
        python3-yaml \
        python3-requests \
        python3-distutils \
        python3-requests

COPY wb_animation_action /usr/lib/python3/dist-packages/wb_animation_action
COPY controllers ${WEBOTS_HOME}/resources/projects/controllers
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
