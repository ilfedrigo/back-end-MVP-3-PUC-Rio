FROM python:3.9-slim

ENV FLASK_APP=app.py

COPY back-end-MVP-3-PUC-Rio/ /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=127.0.0.1"]