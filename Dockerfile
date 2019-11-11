# Multi stage build

FROM python:3.7-slim-buster AS builder

COPY entrypoint.sh /opt
COPY requirements.txt /opt

RUN apt-get update \
    && echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections \
    # install packages
    && apt-get -qq install --no-install-recommends \
        gcc \
        # required for download pypy
        wget \
        bzip2 \
        libgraphviz-dev \
    && pip wheel \
        --wheel-dir=/opt/wheelhouse \
        -r /opt/requirements.txt \
    # pypy install
    && wget  -O /tmp/pypy.tar.bz2 https://bitbucket.org/pypy/pypy/downloads/pypy3.6-v7.2.0-linux64.tar.bz2 \
    && tar xjf /tmp/pypy.tar.bz2 -C /opt \
    # && wget -O /tmp/im.tar.bz2 ftp://ftp.imagemagick.org/pub/ImageMagick/ImageMagick-7.0.9-2.tar.bz2 \
    # && cd /opt/ImageMagick-7.0.9-2 \
    # && ./configure --without-x --prefix=/opt/local \
    # && make \
    # && make install
    && echo "next"


FROM python:3.7-slim-buster

# copy app in one layer
COPY --from=builder /opt /opt

RUN apt-get update \
    && echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections \
    # install packages
    && apt-get -qq install --no-install-recommends \
        gcc \
        g++ \
        cmake \
        gosu \
        # required for pypy
        libtinfo5 \
        # graphviz
        graphviz \
        imagemagick \
    && pip install --upgrade pip \
    # install wheels
    && pip install \
        --no-cache-dir \
        --no-index \
        --find-links=/opt/wheelhouse \
        -r /opt/requirements.txt \
    # link
    && ln -s /opt/pypy3.6-v7.2.0-linux64/bin/pypy3 /usr/local/bin \
    && chmod a+x /opt/entrypoint.sh \
    # clean
    && rm -rf /opt/wheelhouse \
    && rm -rf /var/lib/apt/lists/* \
    # add user
    && useradd -ms /bin/sh benchmarker


ENV PYTHONUNBUFFERED=1 \
    PATH="${PATH}:/opt/benchmark"

ENTRYPOINT [ "/opt/entrypoint.sh" ]
CMD ["sleep", "infinity"]
