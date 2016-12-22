
FROM debian:latest

MAINTAINER Miles Lacey

RUN groupadd hambot
RUN useradd -ms /bin/bash -g hambot hambot

USER hambot
WORKDIR /home/hambot

COPY postgres_setup.bash /home/hambot
CMD chmod 674 ./postgres_setup.bash
RUN bash ./postgres_setup.bash -h


