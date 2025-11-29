from app import app, db
from sqlalchemy import text
from flask import request
from model.category import Category
from flask_jwt_extended import jwt_required


@app.get('/category/list')
@jwt_required()
def category():
    sql = text("""SELECT * FROM  category""")
    result = db.session.execute(sql).fetchall()
    rows = [dict(row._mapping) for row in result]
    return rows, 200


@app.get('/category/list-by-id/<int:category_id>')
@jwt_required()
def category_by_id(category_id):
    result = get_category_by_id(category_id)
    return result


@app.post('/category/create')
@jwt_required()
def create_category():
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

    category_name = form.get('name')

    category = Category(
        name=category_name,
        image=file_name
    )
    db.session.add(category)
    db.session.commit()

    return {
               "message": "Category created",
               "category": get_category_by_id(category.id)
           }, 200


@app.post('/category/update')
@jwt_required()
def update_category():
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

    category = Category.query.get(category_id)
    category.name = category_name
    if image:
        category.image = file_name

    # assert False, f"{file_name}, {category_name}"
    db.session.commit()

    return {
               "message": "category updated",
               "category": get_category_by_id(category_id)
           }, 200


@app.post('/category/delete')
@jwt_required()
def delete_category():
    form = request.get_json()
    if not form.get('category_id'):
        return {"error": "Category ID is required"}, 400
    is_existing = get_category_by_id(form.get('category_id'))
    if is_existing.get('error'):
        return {"error": "Category not found"}, 404
    
    category_id = form.get('category_id')
    category = Category.query.get(category_id)
    db.session.delete(category)
    db.session.commit()

    return {
               "message": "category deleted",
           }, 200


def get_category_by_id(category_id: int) -> dict:
    sql = text("""SELECT * FROM  category WHERE  id = :category_id""")
    result = db.session.execute(sql, {"category_id": category_id}).fetchone()
    if result:
        return dict(result._mapping)
    return {
        "error": "Category not found"
    }
