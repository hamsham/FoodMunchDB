
FROM debian:latest

MAINTAINER Miles Lacey

ENV DB_USER hambot

ENTRYPOINT ["/bin/bash", "-c"]

RUN apt-get update
RUN apt-get -y install sudo curl

RUN groupadd "$DB_USER"
RUN useradd -ms /bin/bash -G root -g "$DB_USER" "$DB_USER"
RUN echo "$DB_USER:$DB_USER" | chpasswd && adduser "$DB_USER" sudo

USER "$DB_USER"
WORKDIR "/home/$DB_USER"

COPY postgres_setup.bash "/home/$DB_USER"
# RUN chown "$DB_USER:$DB_USER" ./postgres_setup.bash
# RUN chmod 674 ./postgres_setup.bash
RUN ./postgres_setup.bash -h


