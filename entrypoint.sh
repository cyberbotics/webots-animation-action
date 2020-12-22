#!/bin/bash

if [ ! -z "${DEBUG}" ]; then
    export GITHUB_REF='/refs/master'
    export GITHUB_ACTOR='cyberbotics'
    export GITHUB_TOKEN='token123'
    export GITHUB_REPOSITORY='cyberbotics/webots-animation-template'
    export BOT_USERNAME='lukicdarkoo-bot'
    export BOT_PAT_KEY='token123'
fi

# Start
python3 -m wb_animation_action
