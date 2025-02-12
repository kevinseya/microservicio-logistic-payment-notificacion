<<<<<<< HEAD
=======
# Usa una imagen base más ligera y adecuada
>>>>>>> ec1ed5a23e64cdc3ccdb3ce7fb2bf7c44b1eea1b
FROM python:3.9.12-slim

# Actualizar los repositorios e instalar las dependencias necesarias para MariaDB
RUN apt-get update && apt-get install -y libmariadb-dev gcc

# Definir el directorio de trabajo
WORKDIR /app

# Copiar solo el archivo de requisitos primero para mejorar el caching
COPY requirements.txt .

# Instalar las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto 5003 (el puerto que usas para Flask)
EXPOSE 5003

# Configurar variables de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Comando para iniciar Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5003"]
