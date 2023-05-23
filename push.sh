#!/bin/sh
if [ "$PASSWORD_MANAGER" = "1password" ]; then
    #shellcheck disable=SC2016
    op run -- zsh -c 'echo $CR_PAT | docker login ghcr.io -u $GH_USERNAME --password-stdin'
else
    echo "$CR_PAT" | docker login ghcr.io -u "$GH_USERNAME" --password-stdin
fi
lowercase_username=$(echo "$GH_USERNAME" | tr '[:upper:]' '[:lower:]')
pip freeze > requirements.txt
docker buildx build --platform linux/amd64 -t "ghcr.io/$lowercase_username/pyreddit:latest" .
docker push "ghcr.io/$lowercase_username/pyreddit:latest"