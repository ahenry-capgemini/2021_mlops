FROM python:3.7-slim

# Dockerfile of the training api
COPY requirements.txt tmp/requirements.txt
RUN pip install -r tmp/requirements.txt 

COPY /app /app

EXPOSE 8000

ENV GIT_PYTHON_REFRESH=quiet

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]