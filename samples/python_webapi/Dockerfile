FROM python:3.6

WORKDIR /app

COPY . .

RUN pip install -e .

CMD ["gunicorn", "randd_sample.api:app", "--config", "guniconf.py"]
