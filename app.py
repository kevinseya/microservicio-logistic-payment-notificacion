import os
from flask import Flask, request, jsonify
from model.models import Notificacion
from repository.repository_mongo import save_notification
from repository.repository_mariadb import get_order_by_id
from repository.repostory_postgres import update_payment_status_ok, get_customer_by_id, get_pay_by_payment_intent
from service.email_service import send_email
from uuid import UUID
from model.models import Payment
from datetime import datetime
from dotenv import load_dotenv
import requests
from pymongo.errors import ConnectionFailure, WriteError


load_dotenv()

app = Flask(__name__)
port = int(os.getenv("PORT", 5000))
url_update_order_status = os.getenv("URL_UPDATE_ORDER_STATUS", "http://localhost:7002/api/order/update")

@app.route("/")
def home():
    return f"Webhook is running on port {port} 🚀"

@app.route("/test-db")
def test_db():
    try:
        from config.mongo import db
        db[os.getenv("MONGO_COLLECTION")].find_one()
        return jsonify({"message": "Connection to MongoDB succesfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error of connection: {str(e)}"}), 500

@app.route("/webhook_update_payment", methods=["POST"])
def webhook():
    """
    Endpoint to receive notifications on webhook and send email.
    """
    try:
        if not request.is_json:
            return jsonify({"error": "JSON content is required"}), 400

        data = request.json
        
        required_fields = ["payment_intent"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Required field missing: {field}"}), 400

        #Update status payment
        data["payment_intent"] = str(data["payment_intent"]) 
        update_payment_status_ok(data["payment_intent"])
       
        try:
            payment = get_pay_by_payment_intent(data["payment_intent"])
            if not payment:
                return jsonify({"error": "Payment not found"}), 404
                        
            order = get_order_by_id(str(payment.order_id))
            if not order:
                return jsonify({"error": "Order not found"}), 404

            #Update statut Order
            update_url = f"{url_update_order_status}/{order['order_id']}"
            payload = {"status": "Paid"}
            response = requests.put(update_url, json=payload)
            if not response:
                return jsonify({"error": "Error updating order"}), 404              
        
            notification_data = {
                "payment_intent": str(data["payment_intent"]),
                "order_id": str(order['order_id']),  
                "payment_id": str(payment.id),  
                "packageDetails": str(order['package_details']),
                "price": str(order["price"]),
                "message": "Update Status to 'PROCESSED' in order",
                "date": datetime.utcnow()
            }


            notification = save_notification(notification_data)

            customer = get_customer_by_id(str(UUID(order["idCustomer"])))
            if not payment:
                return jsonify({"error": "Customer not found"}), 404
           
        except (ConnectionFailure, WriteError) as e:
            return jsonify({"error": f"Error of database: {str(e)}"}), 503
        
        email_sent = send_email(
    recipient=str(customer["email"]),
    subject="Order Payment Notification",
    body=f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    background-color: #ffffff;
                    border-radius: 10px;
                    padding: 25px;
                    max-width: 500px;
                    margin: auto;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    text-align: center;
                }}
                h1 {{
                    color: #333;
                    font-size: 22px;
                    margin-bottom: 15px;
                }}
                p {{
                    color: #555;
                    font-size: 16px;
                    line-height: 1.6;
                    margin: 8px 0;
                }}
                .highlight {{
                    color: #007BFF;
                    font-weight: bold;
                }}
                .payment-box {{
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                    margin-top: 15px;
                    text-align: left;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 14px;
                    color: #777;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎉 Payment Confirmed! 🎉</h1>
                <p>Hola <strong class="highlight">{customer["name"]}</strong> <strong class="highlight">{customer["lastname"]}</strong>,</p>
                <p>Hemos recibido tu pago exitosamente. Aquí tienes los detalles:</p>
                
                <div class="payment-box">
                    <p><strong>💳 ID de Pago:</strong> <span class="highlight">{notification_data["payment_id"]}</span></p>
                    <p><strong>📅 Date:</strong> <span class="highlight">{notification_data["date"]}</span></p>
                    <p><strong>🔗 Method:</strong> <span class="highlight">Stripe</span></p>
                    <p><strong>💰 Amount:</strong> <span class="highlight">{notification_data["price"]}</span></p>
                    <p><strong>📦 Order:</strong> <span class="highlight">{notification_data["order_id"]}</span></p>
                    <p><strong>📝 Details:</strong> <span class="highlight">{notification_data["packageDetails"]}</span></p>
                </div>

                <p class="footer">Gracias por tu compra. ¡Esperamos verte pronto! 😊</p>
            </div>
        </body>
    </html>
    """,
    is_html=True  
)

        
        response = {
            "message": "Notification received and mail sent" if email_sent else "Notification received but mail failed to send",
            "data": notification,
            "email_status": "sent" if email_sent else "failed"
        }
        
        return jsonify(response), 201
            
    except ValueError as e:
        return jsonify({"error": f"Validation error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    print(f"Webhook is running on port {port} 🚀")
    app.run(debug=True, host="0.0.0.0", port=port)
