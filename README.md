# microservicio-logistic-payment-notificacion
# Python Project: Logistics Payment Notification

## microservice-logistic-payment-notification

This is a microservice developed in **Python** that provides an API to manage payment notifications in a logistics system. Its main functionality is to receive payment confirmations, update order statuses, and send email notifications to customers.

## Prerequisites

Make sure you have the following installed on your system:

- **Python** (v3.8 or higher)
- **Docker**
- **MongoDB** (for storing notifications)
- **MariaDB / PostgreSQL** (if relational storage is required)
- Setting up an SMTP server for sending emails

## Setup

### 1. Clone the repository

If the project is hosted on a Git repository, clone it to your local machine:

```sh
git clone https://github.com/kevinseya/microservicio-logistic-payment-notificación.git
```

### 2. Set up environment variables

Create a `.env` file in the root of the project with the following variables:

```sh
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=db_notifications
MONGO_COLLECTION=notifications
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
PORT=5003
```

### 3. Install dependencies

Run the following command to install the necessary dependencies:

```sh
pip install -r requirements.txt
```

### 4. Run the project

To run the server locally, use the following command:

```sh
python app.py
```

The server will start on port **5003**. You can test it with:

```
http://localhost:5003
```

## Project Structure

```
.microservice-logistic-payment-notification/
├── .github/workflows/dockerhub_ec2.yml # CI/CD Configuration
├── config/
│ ├── config.py # Environment Variables Configuration
│ ├── mariadb.py # Connection to MariaDB
│ ├── mongo.py # Connection to MongoDB
│ ├── postgresql.py # Connection to PostgreSQL
├── model/
│ ├── models.py # Data Models
├── repository/
│ ├── repository_mariadb.py # Logic for MariaDB queries
│ ├── repository_mongo.py # Logic for MongoDB queries
│ ├── repository_postgres.py # Logic for PostgreSQL queries
├── service/
│ ├── email_service.py # Service for sending emails
├── .gitignore
├── Dockerfile # Docker configuration
├── requirements.txt # Project dependencies
├── app.py # Application entry point
└── README.md
```

## CI/CD with Docker and EC2

This microservice is configured to be deployed on **AWS EC2** via GitHub Actions.

### 1. Building and Pushing Image to Docker Hub

The `.github/workflows/dockerhub_ec2.yml` file contains the steps to:
- Authenticate to Docker Hub
- Build the image with `docker build`
- Push it to Docker Hub with `docker push`

### 2. Deploy to EC2

- The EC2 instance fetches the image from Docker Hub
- Any previous containers are stopped and removed
- A `.env` file is generated with the necessary credentials
- The container is started with `docker run`

## Docker

To build and run the microservice in Docker manually:

### 1. Build the image
```sh
docker build -t payment_notification .
```

### 2. Run the container
```sh
docker run -d --name payment_notification -p 5003:5003 --env-file .env payment_notification
```

## Endpoints API

### Payment Notification Webhook
- **Path:** `POST /webhook_update_payment`
- **Body:**

```json
{
 "payment_intent": "pi_1234567890"
}
```

- **Answer:**
```json
{
 "message": "Notification received and mail sent",
 "data": {"payment_id": "pi_1234567890", "order_id": "ord_789456", ...},
 "email_status": "sent"
}
```

## Technologies Used

- **Python** as main language
- **MongoDB** for storing notifications
- **MariaDB / PostgreSQL** for storing payments and orders
- **Flask-Mail** for sending emails
- **Docker** for containerization
- **GitHub Actions** for CI/CD
- **AWS EC2** for cloud deployment

