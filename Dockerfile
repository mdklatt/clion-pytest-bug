FROM ubuntu:22.04

RUN apt-get update \
  && apt-get install --yes  \
    ssh \
    build-essential \
    gcc \
    g++ \
    gdb \
    cmake \
    libbrotli-dev \
  && apt-get clean
