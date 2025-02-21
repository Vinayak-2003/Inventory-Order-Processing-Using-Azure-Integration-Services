import azure.functions as func
import logging
from database import create_connection
from uuid import uuid4
import json

receive_order = func.Blueprint()

@receive_order.service_bus_topic_output(arg_name="notification",
                                        connection="usecase1_SERVICEBUS",
                                        topic_name="notification-topic")
@receive_order.route(route="input_order", auth_level=func.AuthLevel.ANONYMOUS)
def input_order(req: func.HttpRequest, notification: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        order = req.get_json()
        
        with create_connection() as conn:
            with conn.cursor() as cursor:
                if req.method == "POST":
                    insert_query = f"""INSERT INTO [dbo].[order_details] 
                                (OrderID, CustomerName, Product, TotalQuantity, Contact, Email, Address, City, PaymentMode)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                    cursor.execute(insert_query,
                                (
                                    str(uuid4()),
                                    order["customer_name"],
                                    order["product"],
                                    order["total_quantity"],
                                    order["contact"],
                                    order["email"],
                                    order["address"],
                                    order["city"],
                                    order["payment_mode"]
                                ))
                    cursor.commit()
                
                    check_availability_query = "SELECT AvailableQuantity FROM dbo.inventory_details WHERE ItemName = (?);"
                    cursor.execute(check_availability_query,
                                (
                                    order["product"]
                                )
                            )
                    row = cursor.fetchone()
                    if row[0] < order["total_quantity"]:
                        return func.HttpResponse(
                            json.dumps({"message": "Stock is less than the required"})
                        )
                        
                else:
                    return func.HttpResponse(
                        json.dumps({"message": f"Method {req.method} cannot operated"})
                    )
                    
        notification.set(order)
                
        return func.HttpResponse(
            json.dumps({"message": "your order is received successfully", "order": order})
        )
    except Exception as err:
        return func.HttpResponse(
            json.dumps({"An error occurred": err})
        )