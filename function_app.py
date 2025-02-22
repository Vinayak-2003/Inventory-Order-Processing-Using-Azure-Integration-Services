import azure.functions as func
import logging

from database import create_order_table, create_inventory_table
from functions.order_receive import receive_order
from functions.servicebus_to_sql import servicebus
from functions.inventory_management import inventory

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
app.register_functions(receive_order)
app.register_functions(servicebus)
app.register_functions(inventory)


create_order_table()
create_inventory_table()