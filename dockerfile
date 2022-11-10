# syntax=docker/dockerfile:1
FROM alpine:3.16.2
LABEL maintainer="jwubben@disca.upv.es"

RUN apk add --no-cache python3
RUN apk add --no-cache openjdk17
RUN apk add git
WORKDIR /workdir
RUN git clone https://github.com/Jamie-Wubben/ardusimMockup.git
WORKDIR /workdir/ardusimMockup
EXPOSE 10000/udp