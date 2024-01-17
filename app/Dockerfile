FROM python:3.11.4-slim-buster

# Path: /app
WORKDIR /app

# Path: /app/requirements.txt
COPY requirements.txt requirements.txt

# Path: /app
RUN pip install -r requirements.txt

# Path: /app
COPY . .

# Path: /app
CMD [ "python", "main.py" ]

# Path: /app
EXPOSE 8000

