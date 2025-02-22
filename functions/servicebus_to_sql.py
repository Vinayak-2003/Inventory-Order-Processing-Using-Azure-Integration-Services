import azure.functions as func
import logging
from database import create_connection
import json
import ast

servicebus = func.Blueprint()

@servicebus.service_bus_topic_trigger(arg_name="azservicebus",
                                        topic_name="notification-topic",
                                        subscription_name="notification-subscription",
                                        connection="usecase1_SERVICEBUS") 
def servicebus_topic_trigger(azservicebus: func.ServiceBusMessage):
    
    try:
        order = azservicebus.get_body().decode('utf-8')
        json_order = json.loads(order)
        
        items = json_order["products"]
        strip_items = items.strip("'")
        json_items = ast.literal_eval(strip_items)
        
        with create_connection() as conn:
            with conn.cursor() as cursor:
                
                for item,quantity in json_items.items():
                    select_query = "SELECT AvailableQuantity, Price, TotalCost FROM dbo.inventory_details WHERE ItemName = (?)"
                    cursor.execute(select_query, (item))
                    row = cursor.fetchone()
                    
                    if row:
                        if row[0] < quantity:
                            print(f"{item} available quantity in less than the required")
                        else:
                            updated_available_quantity = row[0] - quantity
                            total_amount = quantity * row[1]
                            updated_total_cost = row[2] - total_amount
                            
                            update_query = "UPDATE dbo.inventory_details SET AvailableQuantity = (?), TotalCost = (?) WHERE ItemName = (?);"
                            cursor.execute(update_query, (updated_available_quantity, updated_total_cost, item))
                            cursor.commit()
                    
                    else:
                        print(f"Item {item} not found")                        
                    
    except Exception as err:
        raise err