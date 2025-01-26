FROM --platform=linux/amd64 python:3.11-slim
EXPOSE 8000
ENV PIP_DEFAULT_TIMEOUT=100
ENV HOST 0.0.0.0
WORKDIR /app
COPY . ./
ENV TMPDIR='/var/tmp'
RUN apt-get update && apt-get install -y build-essential
RUN pip install -r requirements.txt
CMD ["python", "app.py"]