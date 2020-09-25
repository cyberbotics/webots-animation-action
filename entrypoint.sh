#!/bin/bash

mkdir /tmp/animation
python3 /bin/scripts/run.py

git config --global user.name ${GITHUB_ACTOR}	
git config --global user.email ${GITHUB_ACTOR}@github.com
git reset --hard
git fetch
git checkout gh-pages || git checkout -b gh-pages
rm -rf $(ls -aI '.git') 2> /dev/null
cp -r /tmp/animation/* .
git add -A
git commit -m "Update simulation"	
git push "https://$GITHUB_ACTOR:$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY"
