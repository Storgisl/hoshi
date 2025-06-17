FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# ---- system deps ----------------------------------------------------------
RUN apt-get update && apt-get install -y \
    tzdata git curl ffmpeg libsndfile1 libgl1 libglib2.0-0 \
    build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

# ---- python deps (cached if requirements.txt unchanged) -------------------
WORKDIR /workspace
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# ---- copy source code last (changes often) --------------------------------
COPY . .

# ---- runtime --------------------------------------------------------------
EXPOSE 5050
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]

