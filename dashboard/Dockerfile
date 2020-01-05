FROM python:3.7.5
WORKDIR /usr/src/app
EXPOSE 8000

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
COPY . /usr/src/app/