FROM python:3.12.3-bullseye
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /nasa
WORKDIR /nasa
COPY requeriments.txt /nasa/
RUN pip install -r requeriments.txt
COPY . /nasa/
CMD python manage.py runserver 0.0.0.0:8080
