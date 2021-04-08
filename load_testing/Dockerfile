
FROM python:3.7

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY test_data.csv test_data.csv
COPY locust.py locust.py

EXPOSE 8089
CMD ["locust", "-f", "locust.py", "--host", "http://serving_api:8001"]
