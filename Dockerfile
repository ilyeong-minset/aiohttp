FROM python:latest
COPY *.html *.js server.py requirements.txt /usr/local/src/
WORKDIR /usr/local/src/
RUN ["pip", "install", "aiohttp", "asyncpg", "aredis", "uvloop"]
ENTRYPOINT ["python", "server.py"]
