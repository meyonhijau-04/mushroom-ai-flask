# Gunakan Python 3.11 slim sebagai base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy semua file ke container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Training model saat build
RUN python train_model.py

# Expose port
EXPOSE 8080

# Jalankan aplikasi
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]