FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN mkdir src
RUN mkdir scripts
RUN mkdir static
COPY src/ /code/src
COPY static/ /code/static
COPY scripts/ /code/scripts
