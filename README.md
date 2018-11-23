# Instacart-Market-Basket-Analysis

## Attributes of each file
aisle.csv -> aisle_id, aisle

departments.csv -> department_id, department

order_products_* .csv -> order_id, product_id, add_to_cart_order, reordered 

orders.csv -> order_id, user_id, eval_set, order_number, order_dow, order_hour_of_day, days_since_prior_order

products.csv -> product_id, product_name, aisle_id, department_id

sample_submission.csv -> order_id, products


## The Data
Link: https://drive.google.com/open?id=1o-Y-niwllW8u5USRlFN0gK0ievWc-6JV

The dataset is a relational set of files describing customers' orders for the year 2017. The dataset is anonymized and contains a sample of over 3 million grocery orders from more than 200 thousand Instacart users. For each user, minimum number of orders is 4 and maximum is 100, with the sequence of products purchased in each order. It also provides information regarding the week and hour of day for a particular order.

Each entity (customer, product, order, aisle, etc.) has an associated unique id. Most of the files and variable names are self-explanatory.

### order_products__* .csv
These files specify which products were purchased in each order. order_products_prior.csv contains previous order contents for all customers. 'reordered' indicates that the customer has a previous order that contains the product. Note that some orders will have no reordered items.

### orders.csv
This file tells to which set (prior, train, test) an order belongs. You are predicting reordered items only for the test set orders. 'order_dow' is the day of week. 


## YouTube Link
Link: https://www.youtube.com/watch?v=MkOsllr-HgM
