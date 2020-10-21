#!/bin/bash

# Install dependencies
python3 /bin/scripts/execute_init.py

# Generate animation
mkdir /tmp/animation
python3 /bin/scripts/generate_animation.py

# Publish animation to `gh-pages` branch
NAME=$(curl https://api.github.com/users/${GITHUB_ACTOR} | jq -r .name)
ID=$(curl https://api.github.com/users/${GITHUB_ACTOR} | jq -r .id)
BRANCH=${GITHUB_REF##*/}
git config --global user.name "${NAME}"
git config --global user.email "${ID}+${GITHUB_ACTOR}@users.noreply.github.com"
git reset --hard
git fetch
git checkout gh-pages || git checkout -b gh-pages
rm -rf ${BRANCH}/*
mkdir -p ${BRANCH}
cp -r /tmp/animation/* ${BRANCH}/
cp /bin/scripts/index_header.html index.html
for dir in */
do
  dir=${dir%*/}
  echo "    <li><a href=\"${dir}\">${dir}</a></li>" >> index.html
done
cat /bin/scripts/index_footer.html >> index.html
git add -A
git commit -m "Updated animation"
git push "https://$GITHUB_ACTOR:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY"
