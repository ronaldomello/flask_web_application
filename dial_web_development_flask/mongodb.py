# Imports

import pymongo
from bson.objectid import ObjectId

# Connection with mongodb

client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@dial.zb7eejk.mongodb.net/?retryWrites=true&w=majority")

# Instantiating

db = client.diAL

# Products collection

products = db.products

# Indexing

products.create_index([("product_name", pymongo.ASCENDING), ("inventory_location", pymongo.ASCENDING)],
                      name="unique_p_name_per_inventory", unique=True)

products.create_index([("product_code", pymongo.ASCENDING), ("inventory_location", pymongo.ASCENDING)],
                      name="unique_p_code_per_inventory", unique=True)


# Utility methods

class MongoUtils:
    """Class for all operations with database"""

    # Select

    def select_product(all=False, forms=False, id=None, name=None):
        if all is True:
            """Return all products into database"""
            products_list = []
            products = db.products.find({})
            for product in products:
                product['_id'] = str(product['_id'])
                products_list.append(product)
            return products_list
        if forms is True:
            """Query product by 'product_name' into database (LIKE), for search forms"""
            products_list = []
            products = db.products.find({"product_name": {'$regex': name}})
            for product in products:
                product['_id'] = str(product['_id'])
                products_list.append(product)
            return products_list
        if id:
            """Query product by 'product_id' into database"""
            product = db.products.find_one({"_id": ObjectId(id)})
            return dict(product)
        return False

    # Insert

    def insert_product(user_id, product_name, product_code, quantity, price, category, inventory_location):
        """Insert product into database"""
        product = {
            "user_id": user_id,
            "product_name": product_name,
            "product_code": product_code,
            "quantity": int(quantity),
            "price": round(float(price), 2),
            "category": category,
            "inventory_location": inventory_location,
            "total_value": round(float(quantity * price), 2),
        }
        products.insert_one(product)

    # Update

    def update_product(id, user_id=None, product_name=None, product_code=None,
                       quantity=None, price=None, category=None, inventory_location=None):
        """Update product into database"""
        if quantity:
            quantity = int(quantity)
        if price:
            price = round(float(price), 2)
        product = MongoUtils.select_product(id=id)
        if product:
            db.products.update_one({"_id": product['_id']},
                                   {"$set": {"user_id": user_id if user_id else product['user_id'],
                                             "product_name": product_name if product_name else product['product_name'],
                                             "product_code": product_code if product_code else product['product_code'],
                                             "quantity": quantity if quantity else product['quantity'],
                                             "price": price if price else product['price'],
                                             "category": category if category else product['category'],
                                             "inventory_location": inventory_location if inventory_location
                                             else product['inventory_location']}})
            if quantity and price:
                db.products.update_one({"_id": product['_id']},
                                       {"$set": {"total_value": round(float(quantity * price), 2)}})
            elif quantity and not price:
                db.products.update_one({"_id": product['_id']},
                                       {"$set": {"total_value": round(float(quantity * product['price']), 2)}})
            elif price and not quantity:
                db.products.update_one({"_id": product['_id']},
                                       {"$set": {"total_value": round(float(product['quantity'] * price), 2)}})

    # Delete

    def delete_product(id):
        """Delete product into database"""
        products.delete_one({"_id": ObjectId(id)})


if __name__ == '__main__':  # For test
    pass
