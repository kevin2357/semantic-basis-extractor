FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY songfinder /app/songfinder
COPY tests /app/tests
ENV PYTHONPATH=/app
WORKDIR /work
ENTRYPOINT ["python", "-m", "songfinder"]
