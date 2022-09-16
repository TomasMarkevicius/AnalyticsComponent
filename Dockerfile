# syntax=docker/dockerfile:1
FROM python:3.8.3
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY . .
CMD ["python3", "__main__.py"]