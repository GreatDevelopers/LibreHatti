FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /Librehatti
WORKDIR /Librehatti
ADD . /Librehatti
COPY ./requirements.txt /Librehatti/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /Librehatti
