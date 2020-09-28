FROM cyberbotics/webots:R2020b-rev1-ubuntu20.04

RUN apt-get update && \ 	
    apt-get install -y git python3-yaml jq

COPY scripts /bin/scripts
COPY controllers ${WEBOTS_HOME}/webots/resources/projects/controllers
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
