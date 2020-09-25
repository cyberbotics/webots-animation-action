FROM cyberbotics/webots 	

RUN apt-get update && \ 	
    apt-get install -y git rsync python3-yaml python3-jinja2 jq

COPY scripts /bin/scripts
COPY controllers ${WEBOTS_HOME}/webots/resources/projects/controllers
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
