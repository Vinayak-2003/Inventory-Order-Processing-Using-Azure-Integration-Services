# Order Processing and Inventory Management System

## Introduction 
This system is designed to manage the inventory and order processing efficiently using Azure services.
- Receiving and storing order details
- Communicating via azure service bus
- Inserting, updating and deleting inventory (manage and update) items using HTTP function

## Components
- Azure function app
- Azure Service bus
- Azure SQL database and Server

## Implementation Steps
1. Order Processing:
- The Order Processing Function App receives an order.
- It stores the order details in Azure SQL Database.
- It sends a message to the Service Bus for inventory update.

2. Inventory Management:
- The Inventory Management Function listens for messages from Service Bus.
- It updates the stock count in Azure SQL Database.
- It marks the order as completed.

## Getting Started
1. Clone the code on VS code.
    git clone <repository_url>
    cd <repository_folder>
2. Python must be setup locally and path must be added.
3. Create a virtual environment as a beter approach using command
    python -m venv {virtual_env_name}
4. Activate the virtual environment using
    {virtual_env_name}\scripts\activate
5. Install the dependencies using
    pip install -r requirements.txt
6. Start the function app using 
    func start