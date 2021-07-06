FROM python:3
MAINTAINER Artem Kurnenkov 'artemkurnenkov@gmail.com'
WORKDIR /code
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN chown -R 65534:65534 /code
USER 65534
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "main_api:app"]
