    FROM python:3.8-slim-buster
    WORKDIR /social_backent
    COPY requirements.txt requirements.txt
    RUN pip install -r requirements.txt
    COPY . .
    CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
