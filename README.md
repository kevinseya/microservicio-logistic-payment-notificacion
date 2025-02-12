# microservicio-logistic-payment-notificacion
# Python Project: Logistics Payment Notification

## microservicio-logistic-payment-notificacion

Este es un microservicio desarrollado en **Python** que proporciona una API para gestionar notificaciones de pago en un sistema logístico. Su funcionalidad principal es recibir confirmaciones de pago, actualizar estados de ordenes y enviar notificaciones por correo electrónico a los clientes.

## Prerrequisitos

Asegúrate de tener instalado lo siguiente en tu sistema:

- **Python** (v3.8 o superior)
- **Docker**
- **MongoDB** (para almacenar notificaciones)
- **MariaDB / PostgreSQL** (si se requiere almacenamiento relacional)
- Configuración de un servidor SMTP para el envío de correos

## Configuración

### 1. Clonar el repositorio

Si el proyecto está alojado en un repositorio de Git, clónalo en tu máquina local:

```sh
git clone https://github.com/kevinseya/microservicio-logistic-payment-notificacion.git
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```sh
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=notificaciones_db
MONGO_COLLECTION=notificaciones
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
PORT=5003
```

### 3. Instalar dependencias

Ejecuta el siguiente comando para instalar las dependencias necesarias:

```sh
pip install -r requirements.txt
```

### 4. Ejecutar el proyecto

Para correr el servidor localmente, usa el siguiente comando:

```sh
python app.py
```

El servidor iniciará en el puerto **5003**. Puedes probarlo con:

```
http://localhost:5003
```

## Estructura del Proyecto

```
.microservicio-logistic-payment-notificacion/
├── .github/workflows/dockerhub_ec2.yml  # Configuración CI/CD
├── config/
│   ├── config.py  # Configuración de variables de entorno
│   ├── mariadb.py  # Conexión a MariaDB
│   ├── mongo.py  # Conexión a MongoDB
│   ├── postgresql.py  # Conexión a PostgreSQL
├── model/
│   ├── models.py  # Modelos de datos
├── repository/
│   ├── repository_mariadb.py  # Lógica para consultas en MariaDB
│   ├── repository_mongo.py  # Lógica para consultas en MongoDB
│   ├── repository_postgres.py  # Lógica para consultas en PostgreSQL
├── service/
│   ├── email_service.py  # Servicio para envío de correos
├── .gitignore
├── Dockerfile  # Configuración de Docker
├── requirements.txt  # Dependencias del proyecto
├── app.py  # Punto de entrada de la aplicación
└── README.md
```

## CI/CD con Docker y EC2

Este microservicio está configurado para ser desplegado en **AWS EC2** mediante GitHub Actions.

### 1. Construcción y subida de imagen a Docker Hub

El archivo `.github/workflows/dockerhub_ec2.yml` contiene los pasos para:
- Autenticar en Docker Hub
- Construir la imagen con `docker build`
- Subirla a Docker Hub con `docker push`

### 2. Despliegue en EC2

- La instancia de EC2 obtiene la imagen de Docker Hub
- Se detiene y elimina cualquier contenedor previo
- Se genera un archivo `.env` con las credenciales necesarias
- Se levanta el contenedor con `docker run`

## Docker

Para construir y correr el microservicio en Docker manualmente:

### 1. Construir la imagen
```sh
docker build -t payment_notification .
```

### 2. Ejecutar el contenedor
```sh
docker run -d --name payment_notification -p 5003:5003 --env-file .env payment_notification
```

## API Endpoints

### Webhook de Notificación de Pago
- **Ruta:** `POST /webhook_update_payment`
- **Cuerpo:**

```json
{
  "payment_intent": "pi_1234567890"
}
```

- **Respuesta:**
```json
{
  "message": "Notification received and mail sent",
  "data": {"payment_id": "pi_1234567890", "order_id": "ord_789456", ...},
  "email_status": "sent"
}
```

## Tecnologías Usadas

- **Python** como lenguaje principal
- **MongoDB** para almacenar notificaciones
- **MariaDB / PostgreSQL** para almacenamiento de pagos y pedidos
- **Flask-Mail** para envío de correos
- **Docker** para contenedorización
- **GitHub Actions** para CI/CD
- **AWS EC2** para despliegue en la nube


