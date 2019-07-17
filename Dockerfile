FROM ubuntu

LABEL maintainer="adrian.lazar95@outlook.com"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

COPY ./requirements.txt /scim/requirements.txt

WORKDIR /scim

RUN pip3 install -r requirements.txt

COPY . /scim

ENTRYPOINT [ "python3" ]

CMD ["run.py"]
