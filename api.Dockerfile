FROM python:3.8
COPY . /init_app
WORKDIR /init_app/api
RUN pip install virtualenv
RUN virtualenv app_venv
RUN app_venv/bin/pip install -r requirements.txt
CMD app_venv/bin/python api.py
