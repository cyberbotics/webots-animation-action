FROM cyberbotics/webots:latest

RUN apt-get update && \ 	
    apt-get install -y git python3-yaml jq

COPY scripts /bin/scripts
COPY controllers ${WEBOTS_HOME}/resources/projects/controllers
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
