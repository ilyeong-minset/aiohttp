From postgres:latest
COPY *.sql /docker-entrypoint-initdb.d/
