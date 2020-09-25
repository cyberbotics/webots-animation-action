FROM cyberbotics/webots 	

RUN apt-get update && \ 	
    apt-get install -y git rsync python3-yaml python3-jinja2

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
