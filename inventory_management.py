import azure.functions as func
import logging
from database import create_connection
from uuid import uuid4
import json

inventory = func.Blueprint()

@inventory.route(route="inventory", auth_level=func.AuthLevel.ANONYMOUS)
def update_inventory(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        item_stock = req.get_json()
        
        with create_connection() as conn:
            with conn.cursor() as cursor:
        
                # to add an item in inventory
                if req.method == "POST":
                    
                    insert_item = """
                        INSERT INTO dbo.inventory_details
                        (ItemID, ItemName, ItemDescription, AvailableQuantity, Price, TotalCost, Vendor, VendorContact)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    cursor.execute(insert_item,
                                (
                                    str(uuid4()),
                                    item_stock["item_name"],
                                    item_stock["item_description"],
                                    item_stock["quantity"],
                                    item_stock["price"],
                                    item_stock["total_cost"],
                                    item_stock["vendor"],
                                    item_stock["vendor_contact"]
                                )
                            )
                    cursor.commit()
                    
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
                                    UPDATE dbo.inventory_details SET AvailableQuantity = (?), Price = (?), TotalCost = (?) WHERE ItemName = (?);
                                    """
                        cursor.execute(update_item,
                                    (
                                        updated_available_quantity,
                                        item_stock["price"],
                                        updated_total_cost,
                                        item_stock["item_name"]
                                    )
                                )
                        cursor.commit()
                
                # to delete an item from the inventory database
                elif req.method == "DELETE":
                    delete_query = "DELETE FROM dbo.inventory_details WHERE ItemName = (?);"
                    cursor.execute(delete_query,
                                (
                                    item_stock["item_name"],
                                )
                            )
                    cursor.commit()
                
                # if the method is other than [POST, UPDATE, DELETE]   
                else:
                    return func.HttpResponse(
                        json.dumps({"message": f"Method {req.method} cannot operated"})
                    )

        return func.HttpResponse(
            json.dumps({"message": f"Inventory updated with {req.method} method"})
        )
    
    except Exception as err:
        return func.HttpResponse(
            json.dumps({"message": f"An error occurred while updating inventory: {err}"})
        )