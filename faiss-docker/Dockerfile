FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/facebookresearch/faiss.git /usr/local/faiss \
    && cd /usr/local/faiss \
    && cmake -B build -S . -DFAISS_ENABLE_GPU=OFF \
    && cmake --build build --target install

CMD ["/bin/bash"]
