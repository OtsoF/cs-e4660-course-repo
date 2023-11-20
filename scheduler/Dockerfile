FROM python:3.11.4

COPY . /app/

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "scheduler.py" ]