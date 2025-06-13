from pymongo.errors import WriteError
from config.mongo import db
from config.config import MONGO_COLLECTION
from model.models import Notificacion
import logging

collection = db[MONGO_COLLECTION]

def save_notification(data):
    """
    Save notification on MongoDB and return object insert.
    """
    try:
        notification = Notificacion(**data)
        result = collection.insert_one(notification.to_dict())
        return {"_id": str(result.inserted_id), **notification.to_dict()}
    except WriteError as e:
        print(f"Error to write on MongoDB: {e}")
        raise
    except Exception as e:
        print(f"Error to save notification: {e}")
        raise