FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN export FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]

