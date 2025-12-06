# Dockerfile
FROM python:3.9-slim

# system deps (for pillow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements first (for caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Ensure TensorFlow version matches the version used to save the model
RUN pip install tensorflow==2.20.0   # <-- update to your TF version
# copy app and model
COPY app.py .
COPY my_binary_class_model.h5 .
COPY templates ./templates
# Cloud Run expects port 8080 by default
ENV PORT=8080

# use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "--workers", "1", "--threads", "8"]
