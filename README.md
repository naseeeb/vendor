Project Name: Vendor Management
Description: It is a vendor management apis which is created using django rest api. This will help in managing vendor , calculating their performances.
This project implements a Django REST framework-based API to manage vendors, purchase orders, and vendor performance.

-------------------------------
## Installation and setup
Please follow these steps to set up the project locally:

1. Clone the repository:git clone https://github.com/naseeeb/vendor.git

2. cd respiratory_name

3.pip install -r requirements.txt

4.python manage.py runserver
-----------------------------------


API Endpoints:

User Registration and Authentication:

app1/api/register/ (POST): Register a new user.

app1/api/login/ (POST): Log in an existing user and obtain access and refresh tokens.
-----------------------------
Vendors:

app1/api/vendors/ (GET, POST): Retrieve all vendors or create a new vendor.

app1/api/vendors/<int:id>/ (GET, PUT, DELETE): Retrieve, update, or delete a specific vendor by ID.
------------------------
Purchase Orders:

app1/api/purchase_orders/ (GET, POST): Retrieve all purchase orders or create a new purchase order.

app1/api/purchase_orders/<str:po_number>/ (GET, PUT, DELETE): Retrieve, update, or delete a specific purchase order by its number.
--------------------
Vendor Performance:

app1/api/vendors/<int:id>/performance/ (GET): Retrieve the performance data for a specific vendor.
--------------------------
API Authentication:

All endpoints except registration and login require JWT authentication. Use the obtained access token in the Authorization header with the format: Bearer <access_token> for authenticated requests.
-------------------------------
Get Aceess Token through Refresh Token:
You can get access token through refresh token.
token/refresh/ (POST): Here is the api end points to access it.
