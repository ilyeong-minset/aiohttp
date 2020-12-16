FROM python:latest
COPY *.html *.js server.py /usr/local/src/
WORKDIR /usr/local/src/
RUN ["pip", "install", "aiohttp"]
ENTRYPOINT ["python", "server.py"]
