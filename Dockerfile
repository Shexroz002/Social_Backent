    FROM python:3.8-slim-buster
    WORKDIR /social_backent
    COPY requirements.txt requirements.txt
    RUN pip install -r requirements.txt
    COPY . .
    CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "social_settings.wsgi:application"]
