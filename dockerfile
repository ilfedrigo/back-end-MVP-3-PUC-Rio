
FROM python:3.9

ENV FLASK_APP=main.py

COPY back-end-MVP-3-PUC-Rio/ /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]