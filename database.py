from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pyodbc
from logs.enable_logging import create_logger
import os
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_CONNECTION_STRING = os.environ["DATABASE_CONNECTION_STRING"]

# create database connection
def create_connection():
    logger = create_logger()
    try:
        conn = pyodbc.connect(DATABASE_CONNECTION_STRING)
        logger.info("database connected successfully!!")
        return conn
    except Exception as err:
        logger.error(f"An error occurred while establishing databse connection: {err}")
        raise err

# order details database
def create_order_table():
    logger = create_logger()
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = '''
            CREATE TABLE dbo.order_details_new(
                [OrderID] UNIQUEIDENTIFIER PRIMARY KEY,
                [CustomerName] VARCHAR(100) NOT NULL,
                [OrderDate] DATETIME DEFAULT GETDATE(),
                [Products] NVARCHAR(500),
                [Contact] VARCHAR(12) NOT NULL,
                [Email] VARCHAR(150) NOT NULL,
                [Address] VARCHAR(500) NOT NULL,
                [City] VARCHAR(50) NOT NULL,
                [PaymentMode] VARCHAR(20) NOT NULL
            );
        '''
        logger.info("Table order_details_new is created succefully")
        cursor.execute(query)
        cursor.commit()
    
    except pyodbc.ProgrammingError as err:
        if '42S01' in str(err):
            logger.info("Table order_details_new is already created!!")
            pass
        else:
            logger.error(f"An error occurred while creating order_details_new table: {err}")
            raise err
    finally:
        logger.info("Database connection is closed successfully!!")
        conn.close()
        
# create inventory table
def create_inventory_table():
    logger = create_logger()
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = '''
            CREATE TABLE dbo.inventory_details(
                [ItemID] UNIQUEIDENTIFIER PRIMARY KEY,
                [ItemName] VARCHAR(50) UNIQUE NOT NULL,
                [ItemDescription] VARCHAR(100) NOT NULL,
                [AvailableQuantity] INT NOT NULL,
                [Price] DECIMAL(6,2) NOT NULL,
                [TotalCost] DECIMAL (10,2) NOT NULL,
                [Vendor] VARCHAR(50) NOT NULL,
                [VendorContact] VARCHAR(12) NOT NULL,
                [InsertedDatetime] DATETIME DEFAULT GETDATE(),
                [LastUpdatedDatetime] DATETIME DEFAULT GETDATE()
            );
        '''
        logger.info("Table inventory_details is created succefully")
        cursor.execute(query)
        cursor.commit()
    
    except pyodbc.ProgrammingError as err:
        if '42S01' in str(err):
            logger.info("Table inventory_details is already created!!")
            pass
        else:
            logger.error(f"An error occurred while creating inventory_details table: {err}")
            raise err
    finally:
        logger.info("Database connection is closed successfully!!")
        conn.close()