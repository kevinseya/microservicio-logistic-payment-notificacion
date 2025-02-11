import os
from dotenv import load_dotenv

load_dotenv()


MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "notificaciones_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "notificaciones")

MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "tu_email@gmail.com")  
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "tu_password")  
MAIL_USE_TLS = True
MAIL_USE_SSL = False

MYSQL_HOST= os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT=os.getenv("MYSQL_PORT", "3306")
MYSQL_USER=os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD", "151610")
MYSQL_DB=os.getenv("MYSQL_DB", "create_user_db")

POSTGRES_HOST= os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT= os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER= os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD= os.getenv("POSTGRES_PASSWORD", "151610")
POSTGRES_DB= os.getenv("POSTGRES_DB", "create_user_db")
