FROM mysql
ENV MYSQL_DATABASE librehatti
COPY ./data/ /docker-entrypoint-initdb.d/
