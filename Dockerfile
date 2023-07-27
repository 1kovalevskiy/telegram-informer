FROM python:3.11
WORKDIR /www
COPY app/requirements.txt /www
RUN pip install -r requirements.txt
COPY ./app /www/app
COPY ./alembic /www/alembic
COPY ./alembic.ini /www
RUN env
#RUN alembic upgrade head
CMD uvicorn app.main:app --host 0.0.0.0 --port 8080