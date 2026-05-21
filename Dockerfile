FROM python:3.12.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    SDL_AUDIODRIVER=dummy

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    xauth \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libx11-6 \
    libxrandr2 \
    libxcursor1 \
    libxi6 \
    libxss1 \
    libxinerama1 \
    libasound2 \
    fontconfig \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

CMD ["sh", "-c", "if [ -n \"$DISPLAY\" ]; then exec python ethnos.py; fi; exec xvfb-run -a python ethnos.py"]