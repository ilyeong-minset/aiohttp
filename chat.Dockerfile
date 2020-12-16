FROM python:latest
COPY chat.html chat.js chat.py /usr/local/src/
WORKDIR /usr/local/src/
RUN ["pip", "install", "aiohttp"]
ENTRYPOINT ["python", "chat.py"]
