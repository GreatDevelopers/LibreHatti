FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /Librehatti
WORKDIR /Librehatti
ADD . /Librehatti
COPY ./requirements1.txt /Librehatti/requirements1.txt
RUN pip install  --upgrade pip && pip install -r requirements1.txt && pip install simplejson
COPY . /Librehatti


