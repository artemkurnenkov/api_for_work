FROM python:3
MAINTAINER Artem Kurnenkov 'artemkurnenkov@gmail.com'
WORKDIR /code
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "main_api:app"]
