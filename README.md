## CHELAI STORE COUNTER
Overview
The Chelai Store Counter is a point-of-sale (POS) application designed to manage sales, inventory, and customer transactions. The application features a user-friendly interface built using Tkinter and connects to a MySQL database to manage product inventory and sales records.

## Features
* Add Items to Cart: Users can add products to their shopping cart with specified quantities.
* Checkout Process: The application calculates the total amount and processes customer payments, providing change if necessary.
* View Products: Users can view current stock, add new products, modify existing products, restock items, and delete products.
* Sales Summary: Users can view daily sales summaries and total sales amount.


## Prerequisites
1. Python 3.x
2. MySQL Server

  
## Required Python libraries:
`pip install mysql-connector-python`


## Install depencies using:
`pip install mysql-connector-python`

## Usage
1.
   python store_app.py
2. *Use the interface to*
    - Add products to the cart by entering the product name and quantity.
    - View the current stock of products.
    - Checkout and process payments.
    - View daily sales summaries.

## Database Structure
  *pydatabase*
    table *inventory*
  - id int primary key auto_increment,
  - Product_Name varchar(255),
  - Price doubble,
  - Stocks int
    table *sales*
  - sale_id primary key auto_increment,
  - total_amount double
  - timestamp timestamp

## Directory Structure
```PYTHON PROJECT\


## License
This project is licensed under the MIT License - see the LICENSE file for details.
