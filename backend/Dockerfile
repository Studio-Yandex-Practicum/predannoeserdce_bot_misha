FROM python:3.11

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY ./devoted_heart/ .

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "devoted_heart.wsgi"]
