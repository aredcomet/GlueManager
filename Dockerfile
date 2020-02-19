FROM python:3.8.1-slim-buster

MAINTAINER GALE Partners "galeblr@galepartners.com"

ENV HOME /root
ENV APP_HOME /application
ENV C_FORCE_ROOT=true
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
        apt-transport-https \
        ca-certificates \
        gnupg \
        curl \
        vim \
        git \
        imagemagick \
        libpq-dev \
        libxml2-dev \
        libxslt1-dev \
        openssh-client \
        file \
        libtiff5-dev \
        libjpeg-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        tcl8.6-dev \
        tk8.6-dev \
        python-tk \
        libncurses5-dev


# Clean up APT and bundler when done.
RUN rm -rf /usr/share/doc \
           /usr/share/man \
           /usr/share/groff \
           /usr/share/info \
           /usr/share/lintian \
           /usr/share/linda \
           /usr/share/locale/ \
           /var/cache/man

# Clean up APT when done.
RUN apt-get clean
RUN apt-get autoclean
RUN apt-get autoremove
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p HOME/.aws/
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME


# Install pip packages
RUN mkdir $APP_HOME/requirements
ADD ./server/requirements/* $APP_HOME/requirements/
RUN pip install -r $APP_HOME/requirements/local.txt
RUN rm -rf requirements
