# Usa una imagen base de Python 3.12 slim
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instala las dependencias necesarias en Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu aplicación al contenedor
COPY src/app.py .

# Exponer el puerto 5000 para la aplicación
EXPOSE 5000

ENV PORT=5000

CMD ["flask", "run", "--host=0.0.0.0"]
