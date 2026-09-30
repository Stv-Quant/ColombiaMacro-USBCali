# Imagen portable: Render (Docker), Google Cloud Run, Fly.io, Railway o un servidor
# de la universidad. Solo sirve el tablero; los datos llegan versionados en el repo.
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8080
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home app && chown -R app /app
USER app
EXPOSE 8080
CMD gunicorn dashboard_colombia:server --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:${PORT}
