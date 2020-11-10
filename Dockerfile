FROM cyberbotics/webots:R2020b-rev1-ubuntu20.04

RUN apt-get update && \ 	
    apt-get install -y git

COPY scripts /bin/scripts
COPY controllers ${WEBOTS_HOME}/webots/resources/projects/controllers
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["python3 wb_animation_action/action.py"]
