FROM node:9.11.1-slim

WORKDIR /code
COPY elm-package.json .
RUN apt-get update && \
    apt-get install -y netbase && \
    npm install -g npm@latest && \
    npm install -g --unsafe-perm elm@0.18.0 && \
    npm install -g --unsafe-perm create-elm-app@1.10.4 && \
    elm package install --yes && \
    apt-get purge -y netbase && \
    rm -rf /var/lib/apt/lists/*

CMD ["elm-app", "start"]
