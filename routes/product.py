from app import app, db
from sqlalchemy import text
from flask import request
from model.product import Product
from routes.category import get_category_by_id


@app.get('/product/list')
def product():
    sql = text("""SELECT * FROM  product""")
    result = db.session.execute(sql).fetchall()
    rows = [dict(row._mapping) for row in result]
    return rows, 200


@app.get('/product/list-by-id/<int:product_id>')
def product_by_id(product_id):
    result = get_product_by_id(product_id)
    return result


@app.post('/product/create')
def product_product():
    form = request.form
    if not form:
        return {"error": "No input data provided"}, 400
    if not form.get('name'):
        return {"error": "product name is required"}, 400
    if not form.get('category_id'):
        return {"error": "category_id is required"}, 400
    if not form.get('cost'):
        return {"error": "cost is required"}, 400
    if not form.get('price'):
        return {"error": "price is required"}, 400
    if not request.files['image']:
        return {"error": "image is required"}, 400

    is_category_existing = get_category_by_id(form.get('category_id'))
    if is_category_existing.get('error'):
        return {"error": "Category not found"}, 404

    image = request.files['image']
    file_name = None
    if image:
        file_name = image.filename
        image.save(f'static/image/product/{file_name}')

    product_name = form.get('name')
    category_id = form.get('category_id')
    cost = form.get('cost')
    price = form.get('price')

    product = Product(
        name=product_name,
        category_id=category_id,
        cost=cost,
        price=price,
        image=file_name
    )
    db.session.add(product)
    db.session.commit()

    return {
               "message": "product created",
               "product": get_product_by_id(product.id)
           }, 200


@app.post('/product/update')
def update_product():
    form = request.form
    image = request.files['image']
    file_name = None
    if image:
        file_name = image.filename
        image.save(f'static/image/category/{file_name}')

    if not form:
        return {"error": "No input data provided"}, 400
    if not form.get('name'):
        return {"error": "CategoryName is required"}, 400

    category_id = form.get('category_id')
    category_name = form.get('name')

    category = Product.query.get(category_id)
    category.name = category_name
    if image:
        category.image = file_name

    # assert False, f"{file_name}, {category_name}"
    db.session.commit()

    return {
               "message": "category updated",
               "category": get_product_by_id(category_id)
           }, 200


@app.post('/product/delete')
def delete_product():
    form = request.get_json()
    if not form.get('category_id'):
        return {"error": "Category ID is required"}, 400
    is_existing = get_product_by_id(form.get('category_id'))
    if is_existing.get('error'):
        return {"error": "Category not found"}, 404
    
    category_id = form.get('category_id')
    category = Product.query.get(category_id)
    db.session.delete(category)
    db.session.commit()

    return {
               "message": "category deleted",
           }, 200


def get_product_by_id(product_id: int) -> dict:
    sql = text("""SELECT * FROM  product WHERE  id = :product_id""")
    result = db.session.execute(sql, {"product_id": product_id}).fetchone()
    if result:
        return dict(result._mapping)
    return {
        "error": "Product not found"
    }
