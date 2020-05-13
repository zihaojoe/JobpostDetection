FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /JobpostDetection/requirements.txt

WORKDIR /JobpostDetection

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install awscli --upgrade

COPY ./upload_data.sh /JobpostDetection/model/upload_data.sh

WORKDIR /JobpostDetection/model

ENTRYPOINT ["sh"]

