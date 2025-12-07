FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY plateforme_donnees/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=plateforme_donnees.settings

EXPOSE 8080

CMD ["gunicorn", "plateforme_donnees.wsgi:application", "--bind", "0.0.0.0:8080"]
