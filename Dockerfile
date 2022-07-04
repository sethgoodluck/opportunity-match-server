FROM python:3.9-slim

WORKDIR /src
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . . 
EXPOSE 3000