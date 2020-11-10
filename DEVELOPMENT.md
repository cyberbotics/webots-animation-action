# Development Guidelines

## Local Development
Build:
```bash
docker build . -t webots-animation-action
```

Pull a sample project:
```bash
git clone https://github.com/cyberbotics/webots-animation-template.git $HOME/webots-animation-template
```

Run:
```bash
docker run \
    -v $HOME/webots-animation-template:/root \
    -w /root \
    -e DEBUG=true \
    -it webots-animation-action
```
