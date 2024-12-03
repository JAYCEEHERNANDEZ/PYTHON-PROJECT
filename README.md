## CHELAI STORE COUNTER
The Chelai Store Counter is a point-of-sale (POS) application designed to manage sales, inventory, and customer transactions. The application features a user-friendly interface built using Tkinter and connects to a MySQL database to manage product inventory and sales records.

## Features
* Add Items to Cart: Users can add products to their shopping cart with specified quantities.
* Checkout Process: The application calculates the total amount and processes customer payments, providing change if necessary.
* View Products: Users can view current stock, add new products, modify existing products, restock items, and delete products.
* Sales Summary: Users can view daily sales summaries and total sales amount.

## Main Functionalities
1. Cart Operations
* Add items to the cart (add_to_cart).
* Remove items from the cart (remove_from_cart).
* Display the current cart contents in a Treeview widget.

2. Product Management
* View stock levels (view_stock).
* Add new products (add_product).
* Restock existing products (restock_product).
* Modify product prices (modify_product).
* Delete products from the database (delete_product).

3. Sales Tracking:
* Process a checkout operation (process_checkout).
* Record sales in the database.
* Display daily sales summary or all sales in a separate window (show_daily_summary).


## Prerequisites
1. Python 3.x
2. MySQL Server

## Required Python libraries:
`pip install mysql-connector-python`

## Install depencies using:
`pip install -r requirements.txt`

## Run the application
`python app.py`

## Usage
1. *Clone Repository*
   ```
   git clone <repository-url>
   cd <repository-folder> ```


2. *Use the interface to*
    - Add products to the cart by entering the product name and quantity.
    - View the current stock of products.
    - Checkout and process payments.
    - View daily sales summaries.

3. *Run the application*
   `python Store_app.py`

## Database Structure
 ```
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
```
## Directory Structure
```
|PYTHON PROJECT\
|
├── Store.app.py # Main application
├── Readme.md # This file
```


## License
This project is licensed under the MIT License - see the LICENSE file for details.
