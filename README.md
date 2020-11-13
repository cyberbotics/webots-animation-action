# Webots Animation Action

This GitHub action creates a Webots animation of a simulation and publishes it to GitHub pages.

<p align="center">
  <img src="./assets/cover.png">
</p>


After each commit, Webots simulation will be recorded and published to `<username>.github.io/<repository>/<branch>` as an X3D animation.
In your browser, you can move around and zoom while the animation is playing.

## Workflow

Here is a simple GitHub workflow snippet which utilizes the action:
```yaml
name: Record animation

jobs:
  record:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repo
        uses: actions/checkout@v2
      - name: Record and deploy the animation
        uses: cyberbotics/webots-animation-action@master
        env: 
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
> You can save the snippet to e.g.: `.github/workflows/record_animation.yml`.

## Configuration

### Demonstration

You can create `webots.yaml` configuration file in the root of your repository to fine tune generated animations.
If the file is not present, the action will automatically generate animations for all files according to the default configuration.

```yaml
type: demo
init: |
  apt install -y \
    python3-numpy \
    python3-opencv
animation:
  worlds:
    - file: worlds/tutorial_6.wbt
      duration: 5
    - file: worlds/tutorial_1.wbt
      duration: 10
```

The options are:

| **name**                      | **description**                                             |
|-------------------------------|-------------------------------------------------------------|
| `init`                        | Init hook used for configuruing and installing dependcies   |
| `type`                        | Project type, can be `demo`, `competition` and `competitor` |
| `animation`                   | Generates Webots animation and publishes to `gh-pages`      |
| `animation.worlds[].file`     | Path to world file (.wbt)                                   |
| `animation.worlds[].duration` | Animation duration in seconds (default 10s)                 |

#### Example
Check out [Webots Animation Template](https://github.com/cyberbotics/webots-animation-template/) repository.

### Competition

> **Warning**: Competitions are under heavy development!
Documentation is not ready and we do not guarantee any backward compatibility.
Please contact us directly if you want to set up a competition at `support@cyberbotics.com`.

#### Organizer

```yaml
type: competition
world: worlds/ratslife_round.wbt
```

Limitations:
- The opposing robots have to have `DEF` field set to `R1` and `R2`.

#### Competitor
```yaml
type: competitor
competition: https://github.com/username/competition
```
