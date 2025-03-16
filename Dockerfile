FROM postgres:latest

WORKDIR /usr/db

RUN apt-get update && \
    apt-get install -y locales && \
    rm -rf /var/lib/apt/lists/*

RUN localedef -i ru_RU -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8

EXPOSE 5432

ENV LANG ru_RU.utf-8
