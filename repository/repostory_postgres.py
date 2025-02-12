import psycopg2
import logging
from model.models import Payment
from config.postgresql import get_postgres_connection_customer, get_postgres_connection_payments

# Function to get payment
def get_pay_by_payment_intent(payment_intent):
    """
    Find the payment according to the payment_intent.
    """
    connection = None
    try:
        connection = get_postgres_connection_payments()
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
                logging.info(f"Payment found: {payment.to_dict()}")
                return payment
            else:
                logging.warning(f"No payment found for payment_intent {payment_intent}")
                return None

    except psycopg2.Error.connector.Error as e:
        logging.error(f"Error getting payment: {e}")
        return None
    finally:
        if connection:
            connection.close()

# Function to get customer information based on customer_id
def get_customer_by_id(customer_id):
    """
    Gets the customer information based on the customer_id.
    """
    connection = None
    try:
        connection = get_postgres_connection_customer()
        with connection.cursor() as cursor:
            # Query to get all customer information based on customer_id
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
                logging.info(f"Client Found: {customer}")
                return customer
            else:
                logging.warning(f"No customer found for customer_id {customer_id}")
                return None

    except psycopg2.Error as e:
        logging.error(f"Error getting client: {e}")
        return None
    finally:
        if connection:
            connection.close()

def update_payment_status_ok(payment_intent):
    """
    Updates the order status in MySQL based on the payment_intent.
    """
    connection = None
    try:
        connection = get_postgres_connection_payments()
        cursor = connection.cursor()

        # Run the status update on the database
        update_query = """
            UPDATE payments
            SET status = %s
            WHERE payment_intent_id = %s
        """
        cursor.execute(update_query, ("PROCESSED", payment_intent))
        connection.commit()

        print(f"Order status updated to PROCESSED for payment_intent {payment_intent}")
        return True

    except psycopg2.Error.Error as e:
        print(f"Error updating order status: {e}")
        return False
    finally:
        if connection:
            connection.close()
