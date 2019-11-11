FROM python:3.7-slim-buster

COPY entrypoint.sh /
COPY requirements.txt /tmp

RUN apt-get update \
    && echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections \
    # install packages
    && apt-get -qq install \
        gcc \
        g++ \
        cmake \
        gosu \
        # required for pypy
        wget \
        bzip2 \
        libtinfo5 \
        # graphviz
        graphviz \
        imagemagick \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    # pypy install
    && wget  -O /tmp/pypy.tar.bz2 https://bitbucket.org/pypy/pypy/downloads/pypy3.6-v7.2.0-linux64.tar.bz2 \
    && tar xjf /tmp/pypy.tar.bz2 -C /opt \
    && ln -s /opt/pypy3.6-v7.2.0-linux64/bin/pypy3 /usr/local/bin \
    && chmod a+x /entrypoint.sh \
    # clean
    && rm -rf /var/lib/apt/lists/* \
    # add user
    && useradd -ms /bin/sh benchmarker

ENV PYTHONUNBUFFERED=1 \
    PATH="${PATH}:/opt/benchmark"

ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["sleep", "infinity"]
