# Development Guidelines

## Local Development
Build:
```bash
docker build . -t webots-animation-action
```

### Animation

Pull a sample project:
```bash
git clone https://github.com/cyberbotics/webots-animation-template.git $HOME/webots-animation-template
```

Run:
```bash
docker run \
    -v $HOME/webots-animation-template:/root/repo \
    -w /root/repo \
    -e DEBUG=true \
    -it webots-animation-action
```

### Competition

Pull a sample project:
```bash
git clone https://github.com/lukicdarkoo/webots-competition-template.git $HOME/webots-competition-template
```

Run:
```bash
docker run \
    -v $HOME/webots-competition-template:/root/repo \
    -w /root/repo \
    -e DEBUG=true \
    -it webots-animation-action
```