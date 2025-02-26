import azure.functions as func
from database import create_connection
from logs.enable_logging import create_logger
from uuid import uuid4
import datetime

inventory = func.Blueprint()

@inventory.route(route="inventory", auth_level=func.AuthLevel.ANONYMOUS)
def update_inventory(req: func.HttpRequest) -> func.HttpResponse:
    logger = create_logger()
    
    try:
        item_stock = req.get_json()
        logger.info("request body is fetched")
        
        with create_connection() as conn:
            with conn.cursor() as cursor:
        
                # to add an item in inventory
                if req.method == "POST":
                    
                    insert_item = """
                        INSERT INTO dbo.inventory_details
                        (ItemID, ItemName, ItemDescription, AvailableQuantity, Price, TotalCost, Vendor, VendorContact)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    total_quantity_cost = item_stock["quantity"] * item_stock["price"]
                    cursor.execute(insert_item,
                                (
                                    str(uuid4()),
                                    item_stock["item_name"],
                                    item_stock["item_description"],
                                    item_stock["quantity"],
                                    item_stock["price"],
                                    total_quantity_cost,
                                    item_stock["vendor"],
                                    item_stock["vendor_contact"]
                                )
                            )
                    cursor.commit()
                    logger.info(f"POST method is executed successfully to insert a new item - {item_stock['item_name']} in the inventory!!")
                    
                # to update an item in the inventory table
                elif req.method == "PUT":
                    check_availability_query = "SELECT AvailableQuantity, TotalCost FROM dbo.inventory_details WHERE ItemName = (?);"
                    cursor.execute(check_availability_query,
                                (
                                    item_stock["item_name"]
                                )
                            )
                    row = cursor.fetchone()
                    updated_available_quantity = row[0] + item_stock["quantity"]
                    updated_total_cost = row[1] + (item_stock["quantity"] * item_stock["price"])
                    
                    # check if the item already exists (unique item only) then update the quantity 
                    if row:
                        update_item = """
                                    UPDATE dbo.inventory_details SET AvailableQuantity = (?), Price = (?), TotalCost = (?), LastUpdatedDatetime = (?) WHERE ItemName = (?);
                                    """
                        cursor.execute(update_item,
                                    (
                                        updated_available_quantity,
                                        item_stock["price"],
                                        updated_total_cost,
                                        datetime.datetime.now(),
                                        item_stock["item_name"]
                                    )
                                )
                        cursor.commit()
                        logger.info(f"PUT method is executed successfully to update an item - {item_stock['item_name']} in the inventory!!")
                
                # to delete an item from the inventory database
                elif req.method == "DELETE":
                    delete_query = "DELETE FROM dbo.inventory_details WHERE ItemName = (?);"
                    cursor.execute(delete_query,
                                (
                                    item_stock["item_name"],
                                )
                            )
                    cursor.commit()
                    logger.info(f"DELETE method is executed successfully to delete an item - {item_stock['item_name']} in the inventory!!")
                
                # if the method is other than [POST, UPDATE, DELETE]   
                else:
                    logger.error(f"{req.method} is not allowed .... change the method to [POST, PUT, DELETE] only")
                    return func.HttpResponse(
                        str({"message": f"Method {req.method} cannot operated .... change the method to [POST, PUT, DELETE] only"})
                    )

        return func.HttpResponse(
            str({"message": f"Inventory updated with {req.method} method"})
        )
    
    except Exception as err:
        logger.error(f"An exception occurred while updating the inventory: {err}")
        return func.HttpResponse(
            str({"message": f"An error occurred while updating inventory: {err}"})
        )