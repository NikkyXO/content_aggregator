FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ENV MYSQL_HOST=localhost
# ENV MYSQL_PORT=3306
# ENV MYSQL_USER=root
# ENV MYSQL_PASSWORD=410208olA$$$
# ENV MYSQL_DATABASE=""

COPY ./app /app