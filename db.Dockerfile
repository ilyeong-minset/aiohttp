FROM postgres:latest
ENV POSTGRES_PASSWORD postgres
COPY *.sql /docker-entrypoint-initdb.d/
