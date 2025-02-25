import azure.functions as func
from database import create_connection
from uuid import uuid4
import ast
from logs.enable_logging import create_logger

receive_order = func.Blueprint()

@receive_order.service_bus_topic_output(arg_name="notification",
                                        connection="usecase1_SERVICEBUS",
                                        topic_name="notification-topic")
@receive_order.route(route="input_order", auth_level=func.AuthLevel.ANONYMOUS)
def input_order(req: func.HttpRequest, notification: func.Out[str]) -> func.HttpResponse:
    logger = create_logger()

    try:

        order = req.get_json()
        logger.info("order is fetched from the request body")

        with create_connection() as conn:
            with conn.cursor() as cursor:
                if req.method == "POST":
                    insert_query = f"""INSERT INTO [dbo].[order_details_new] 
                                (OrderID, CustomerName, Products, Contact, Email, Address, City, PaymentMode)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                    cursor.execute(insert_query,
                                (
                                    str(uuid4()),
                                    order["customer_name"],
                                    order["products"],
                                    order["contact"],
                                    order["email"],
                                    order["address"],
                                    order["city"],
                                    order["payment_mode"]
                                )
                            )
                    cursor.commit()
                    logger.info(f"Order for user - {order['customer_name']} is accepted!!")
                    
                    items = order["products"]
                    strip_items = items.strip("'")
                    json_items = ast.literal_eval(strip_items)
                    
                    for item,quantity in json_items.items():
                        check_availability_query = "SELECT AvailableQuantity FROM dbo.inventory_details WHERE ItemName = (?);"
                        cursor.execute(check_availability_query,
                                    (
                                        item
                                    )
                                )
                        row = cursor.fetchone()
                        if row[0] < quantity:
                            return func.HttpResponse(
                                {"message": f"{item} stock is less than the required"}
                            )
                        
                else:
                    logger.error(f"Method {req.method} cannot operated")
                    return func.HttpResponse(
                        str({"message": f"Method {req.method} cannot operated"})
                    )
                    
        notification.set(order)
        logger.info(f"{order} sent to service bus")

        return func.HttpResponse(
            str({"message": "your order is received successfully", "order": order})
        )
    except Exception as err:
        logger.error(f"An exception occurred while receiving order: {err}")
        return func.HttpResponse(
            str({"An error occurred": err})
        )