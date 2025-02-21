import azure.functions as func
import logging
from database import create_connection
from uuid import uuid4
import json

servicebus = func.Blueprint()

@servicebus.service_bus_topic_trigger(arg_name="azservicebus",
                                        topic_name="notification-topic",
                                        subscription_name="notification-subscription",
                                        connection="usecase1_SERVICEBUS") 
def servicebus_topic_trigger(azservicebus: func.ServiceBusMessage):
    
    try:
        order = azservicebus.get_body().decode('utf-8')
        json_order = json.loads(order)
        
        item = json_order["product"]
        quantity = json_order["total_quantity"]
        
        with create_connection() as conn:
            with conn.cursor() as cursor:
                select_query = "SELECT AvailableQuantity, Price, TotalCost FROM dbo.inventory_details WHERE ItemName = (?)"
                cursor.execute(select_query, (item))
                row = cursor.fetchone()
                
                if row:
                    if row[0] < quantity:
                        pass
                    else:
                        updated_available_quantity = row[0] - quantity
                        total_amount = quantity * row[1]
                        updated_total_cost = row[2] - total_amount
                
                else:
                    print(f"Item {item} not found")
                    
                update_query = "UPDATE dbo.inventory_details SET AvailableQuantity = (?), TotalCost = (?) WHERE ItemName = (?);"
                cursor.execute(update_query, (updated_available_quantity, updated_total_cost, item))
                cursor.commit()
                
    except Exception as err:
        raise err