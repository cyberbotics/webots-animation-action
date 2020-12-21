#!/bin/bash

if [ ! -z "${DEBUG}" ]; then
    export GITHUB_REF='/refs/master'
    export GITHUB_ACTOR='cyberbotics'
    export GITHUB_TOKEN='token123'
    export GITHUB_REPOSITORY='cyberbotics/webots-animation-template'
    export DEPLOY_KEY='-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACCQq78WZE0i9CVst1pf/k3UyJtEBUDcUHOo1gjpj5yMpQAAAJgwCOCoMAjg
qAAAAAtzc2gtZWQyNTUxOQAAACCQq78WZE0i9CVst1pf/k3UyJtEBUDcUHOo1gjpj5yMpQ
AAAEBd+KkVVvJXl70gIBN/aUg1RGUp/I4VsNNiNKNQmpjfGZCrvxZkTSL0JWy3Wl/+TdTI
m0QFQNxQc6jWCOmPnIylAAAAFWx1a2ljZGFya29vQGdtYWlsLmNvbQ==
-----END OPENSSH PRIVATE KEY-----
'
fi

python3 -m wb_animation_action
