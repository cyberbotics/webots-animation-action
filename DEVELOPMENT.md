# Development Guidelines

## Local Development
```bash
docker build . -t webots-animation-action

docker run --env DEBUG=true -it webots-animation-action /bin/bash
```