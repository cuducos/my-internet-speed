FROM node:9.11.1-slim

WORKDIR /code
COPY elm-package.json .
RUN echo "tcp	6	TCP		# transmission control protocol" > /etc/protocols
RUN npm install -g npm@latest && \
    npm install -g --unsafe-perm elm@0.18.0 && \
    npm install -g --unsafe-perm create-elm-app@1.10.4 && \
    elm package install --yes

CMD ["elm-app", "start"]
