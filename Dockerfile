FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ffmpeg \
        portaudio19-dev \
        espeak \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --default-timeout=100 -r /app/requirements.txt

COPY . /app

RUN chmod +x /app/start.sh

EXPOSE 8000 8501

CMD ["/app/start.sh"]
