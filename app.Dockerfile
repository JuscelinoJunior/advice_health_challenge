FROM python:3.8
COPY . /init_app
WORKDIR /init_app/app
CMD python3 -m http.server
