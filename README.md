# Webots Animation Action

This GitHub action creates a Webots animation of a simulation and publishes it to GitHub pages.

<p align="center">
  <img src="./assets/cover.png">
</p>

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

You can check [Webots Animation Template](https://github.com/cyberbotics/webots-animation-template/) repository.
