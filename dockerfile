# syntax=docker/dockerfile:1
FROM alpine:3.16.2
LABEL maintainer="jwubben@disca.upv.es"

RUN apk update
RUN apk add --no-cache python3
RUN apk add --no-cache py-pip
RUN apk add --no-cache openjdk17
RUN apk add git
RUN pip install zmq
WORKDIR /workdir
RUN git clone https://github.com/Jamie-Wubben/ardusimMockup.git
WORKDIR /workdir/ardusimMockup
RUN chmod +x ./start.sh
RUN chmod +x ./stop.sh
CMD ./start.sh