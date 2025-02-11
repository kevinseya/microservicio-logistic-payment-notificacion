import psycopg2
import logging
from model.models import Payment
from config.postgresql import get_postgres_connection

# Función para obtener payment
def get_pay_by_payment_intent(payment_intent):
    """
    Encontrar el pago de acuerdo al payment_intent.
    """
    connection = None
    try:
        connection = get_postgres_connection()
        with connection.cursor() as cursor:  
            select_query = """
                SELECT * FROM payments
                WHERE payment_intent_id = %s
            """
            cursor.execute(select_query, (payment_intent,))
            result = cursor.fetchone()

            if result:
                
                payment = Payment(
                    id=result[0],
                    order_id=result[1],
                    amount=result[2],
                    currency=result[3],
                    status=result[4],
                    payment_intent_id=result[5]
                )
                logging.info(f"Pago encontrado: {payment.to_dict()}")
                return payment
            else:
                logging.warning(f"No se encontró ningún pago para el payment_intent {payment_intent}")
                return None

    except psycopg2.Error.connector.Error as e:
        logging.error(f"Error al obtener el pago: {e}")
        return None
    finally:
        if connection:
            connection.close()

# Función para obtener la información del cliente basado en el customer_id
def get_customer_by_id(customer_id):
    """
    Obtiene la información del cliente basada en el customer_id.
    """
    connection = None
    try:
        connection = get_postgres_connection()
        with connection.cursor() as cursor:
            # Query para obtener toda la información del cliente basado en el customer_id
            select_query = """
                SELECT id, name, lastname, email, phone, password, address, active
                FROM customer
                WHERE id = %s
            """
            cursor.execute(select_query, (customer_id,))
            result = cursor.fetchone()

            if result:
                customer = {
                    "id": result[0],
                    "name": result[1],
                    "lastname": result[2],
                    "email": result[3],
                    "phone": result[4],
                    "password": result[5],
                    "address": result[6],
                    "active": result[7]
                }
                logging.info(f"Cliente encontrado: {customer}")
                return customer
            else:
                logging.warning(f"No se encontró ningún cliente para el customer_id {customer_id}")
                return None

    except psycopg2.Error as e:
        logging.error(f"Error al obtener el cliente: {e}")
        return None
    finally:
        if connection:
            connection.close()

def update_payment_status_ok(payment_intent):
    """
    Actualiza el estado de la orden en MySQL basado en el payment_intent.
    """
    connection = None
    try:
        connection = get_postgres_connection()
        cursor = connection.cursor()

        # Ejecutar la actualización de estado en la base de datos
        update_query = """
            UPDATE payments
            SET status = %s
            WHERE payment_intent_id = %s
        """
        cursor.execute(update_query, ("PROCESSED", payment_intent))
        connection.commit()

        print(f"Estado de la orden actualizado a PROCESSED para el payment_intent {payment_intent}")
        return True

    except psycopg2.Error.Error as e:
        print(f"Error al actualizar el estado de la orden: {e}")
        return False
    finally:
        if connection:
            connection.close()
