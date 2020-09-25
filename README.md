# Webots Animation Action

This GitHub action creates a Webots animation of a simulation and publishes it to GitHub pages.

<p align="center">
  <img src="./assets/cover.png">
</p>


After each commit, Webots simulation will be recorded and published to `<username>.github.io/<repository>` as an X3D animation.
In your browser, you can move around and zoom while the animation is playing.

## Workflow

Here is a simple GitHub workflow snippet which utilizes the action:
```yaml
name: Record animation

on: [push]

jobs:
  record:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repo
        uses: actions/checkout@v2
      - name: Record and deploy the animation
        uses: cyberbotics/webots-animation-action@master
```
> You can save the snippet to e.g.: `.github/workflows/record_animation.yml`.

## Examples

Check out [Webots Animation Template](https://github.com/cyberbotics/webots-animation-template/) repository.
