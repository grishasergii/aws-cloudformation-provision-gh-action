FROM python:3.9-slim-buster

RUN apt-get update
RUN apt-get install -y curl unzip

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /github/workspace

COPY . .
RUN pipenv sync

ENTRYPOINT pipenv run python action/provision.py