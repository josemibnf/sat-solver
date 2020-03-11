FROM ubuntu:latets
FROM python:3.6

RUN apt-get update
RUN apt-get install python3.6-tk
RUN apt-get install python3-pip
RUN pip3 install matplotlib