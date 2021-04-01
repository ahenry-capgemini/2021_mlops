FROM python:3.8

COPY requirements.txt tmp/requirements.txt
RUN pip install -r tmp/requirements.txt

COPY ./app /app

EXPOSE 81

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "81"]