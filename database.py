from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pyodbc

TENANT_ID = "27282fdd-4c0b-4dfb-ba91-228cd83fdf71"
DATABASE_CONNECTION_STRING = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:usecase-1.database.windows.net,1433;Database=usecase-1;Uid=vinayak;Pwd={Usecase001};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

credential = DefaultAzureCredential(authority=f"https://login.microsoftonline.com/{TENANT_ID}")

# create database connection
def create_connection():
    try:
        conn = pyodbc.connect(DATABASE_CONNECTION_STRING)
        return conn
    except Exception as e:
        raise e

# order details database
def create_order_table():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = '''
            CREATE TABLE dbo.order_details(
                [OrderID] UNIQUEIDENTIFIER PRIMARY KEY,
                [CustomerName] VARCHAR(100) NOT NULL,
                [OrderDate] DATETIME DEFAULT GETDATE(),
                [Products] NVARCHAR(500),
                [Contact] VARCHAR(12) NOT NULL,
                [Email] VARCHAR(150) NOT NULL,
                [Address] VARCHAR(500) NOT NULL,
                [City] VARCHAR(50) NOT NULL,
                [TotalAmount] DECIMAL(10,2) NOT NULL,
                [PaymentMode] VARCHAR(20) NOT NULL
            );
        '''
        cursor.execute(query)
        cursor.commit()
    
    except pyodbc.ProgrammingError as err:
        if '42S01' in str(err):
            pass
        else:
            raise err
    finally:
        conn.close()
        
# create inventory table
def create_inventory_table():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = '''
            CREATE TABLE dbo.inventory_details(
                [ItemID] UNIQUEIDENTIFIER PRIMARY KEY,
                [ItemName] VARCHAR(50) NOT NULL,
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
        cursor.execute(query)
        cursor.commit()
        
    except pyodbc.ProgrammingError as err:
        if '42S01' in str(err):
            pass
        else:
            raise err
        
    finally:
        conn.close()
