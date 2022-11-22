
FROM python:3.10.6

# set work directory
WORKDIR /auger

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .