# Online store REST API
##### _Interview project for Childish Ltd._

![N|Solid](https://www.childish.eu/img/logo-gray.png)

---
## Description
A REST API for an online store that provides CRUD endpoints for products 
and orders. The API also provides a statistics endpoint, which displays the
revenue and number of items sold in a specified daterange.

## Please Note
1. As there was no specification provided in the assignment, when creating 
a new order it can be directly populated with products. 
If a product with the same title already exists in the database it 
will be added to the order directly, instead of creating a new instance, as 
to avoid needlesly crowding the database. Note that if the products price 
differs from the original it will be updated and the change will be reflected 
in all other orders where the updated product is present.

2. The swagger documentation can be accessed through: http://127.0.0.1:8000/swagger/schema/

3. The models have been added to the admin page with 'title' and 'price' fields for 
the Product model, and 'id', 'date', 'number of products', and 'revenue' fields
for the Order model.
