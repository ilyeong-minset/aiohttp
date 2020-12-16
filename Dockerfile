FROM python:latest
COPY *.html *.js server.py requirements.txt /usr/local/src/
WORKDIR /usr/local/src/
RUN ["pip", "install", "-r", "requirements.txt"]
ENTRYPOINT ["python", "server.py"]
