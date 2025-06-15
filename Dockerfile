FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
RUN apt-get update && apt-get install -y \
    tzdata \
    git curl ffmpeg libsndfile1 libgl1 libglib2.0-0 \
    build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . .

RUN pip install --upgrade pip setuptools wheel && \
    pip install -U git+https://github.com/facebookresearch/audiocraft#egg=audiocraft && \
    pip install flask && \
    pip install flask-cors

RUN python app/generate_music.py --dry-run || true

EXPOSE 5050

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
