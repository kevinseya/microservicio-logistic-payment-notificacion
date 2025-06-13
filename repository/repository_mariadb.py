import mysql.connector
from config.mariadb import get_mariadb_connection
import logging
from uuid import UUID

logging.basicConfig(level=logging.INFO)

def get_order_by_id(order_id):
    """
    Gets the order information based on the order_id.
    """
    connection = None
    try:
        connection = get_mariadb_connection()
        with connection.cursor() as cursor:
            select_query = """
                SELECT orderId, idCustomer, senderName, receiverName, receiverPhone, 
                       packageDetails, shippingAddress, deliveryAddress, price, status
                FROM orders
                WHERE orderId = %s
            """
            cursor.execute(select_query, (order_id,))
            result = cursor.fetchone()

            if result:
                order = {
                    "order_id": result[0],
                    "idCustomer": result[1],
                    "sender_name": result[2],
                    "receiver_name": result[3],
                    "receiver_phone": result[4],
                    "package_details": result[5],
                    "shipping_address": result[6],
                    "delivery_address": result[7],
                    "price": result[8],
                    "status": result[9]
                }
                logging.info(f"Order found: {order}")
                return order
            else:
                logging.warning(f"No order found for order_id{order_id}")
                return None

    except mysql.connector.Error as e:
        logging.error(f"Error al obtener la orden: {e}")

        return None
    finally:
        if connection:
            connection.close()
