FROM python:3.12
LABEL org.opencontainers.image.source="https://github.com/moevm4388/hestia"

COPY . /app
WORKDIR /app

ENTRYPOINT ["python", "-m", "hestia.main"]
