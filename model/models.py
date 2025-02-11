from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID

class Notificacion(BaseModel):
    payment_id: UUID
    order_id: UUID
    payment_id: str
    packageDetails: str
    price: float
    message: str
    date: datetime

    def to_dict(self):
        return {
            "payment_id": str(self.payment_id), 
            "order_id": str(self.order_id),
            "payment_id": self.payment_id,
            "packageDetails": self.packageDetails,
            "price": self.price,
            "message": self.message,
            "date": self.date.isoformat()
        }
    
class Payment(BaseModel):
    id: UUID
    order_id: UUID
    amount: float
    currency: str
    status: str
    payment_intent_id: str

    def to_dict(self):
        """
        Convierte el modelo en un diccionario para fácil uso en la aplicación.
        """
        return {
            "id": str(self.id),
            "order_id": str(self.order_id),
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "payment_intent_id": self.payment_intent_id
        }