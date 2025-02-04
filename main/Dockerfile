# Imagen Python
FROM python:3.12.3-alpine3.20

# Directorio en el que se crea la imagen
WORKDIR /app

# Paquetes
RUN apk update && \
    apk add --no-cache build-base python3-dev && \
    pip install --upgrade pip

# Dependencias
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Correr aplicacion
COPY ./ ./
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]