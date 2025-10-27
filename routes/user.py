from app import app, db
from sqlalchemy import text
from flask import request
from model.user import User
from werkzeug.security import generate_password_hash, check_password_hash


@app.get('/user/list')
def user():
    sql = text("""SELECT * FROM  user""")
    result = db.session.execute(sql).fetchall()
    rows = [dict(row._mapping) for row in result]
    return rows, 200


@app.get('/user/list-by-id/<int:user_id>')
def user_by_id(user_id):
    result = get_user_by_id(user_id)
    return result


@app.post('/user/create')
def create_user():
    form = request.form
    profile = request.files['profile']
    file_name = None
    if profile:
        file_name = profile.filename
        profile.save(f'static/image/user/{file_name}')

    if not form:
        return {"error": "No input data provided"}, 400
    if not form.get('user_name'):
        return {"error": "UserName is required"}, 400
    if not form.get('password'):
        return {"error": "Password is required"}, 400

    user_name = form.get('user_name')
    password = generate_password_hash(form.get('password'))
    user = User(
        user_name=user_name,
        password=password,
        profile=file_name
    )
    db.session.add(user)
    db.session.commit()

    return {
               "message": "User created",
               "user": get_user_by_id(user.id)
           }, 200


@app.post('/user/update')
def update_user():
    form = request.get_json()
    if not form:
        return {"error": "No input data provided"}, 400
    if not form.get('user_id'):
        return {"error": "User ID is required"}, 400
    if not form.get('user_name'):
        return {"error": "UserName is required"}, 400

    is_existing = get_user_by_id(form.get('user_id'))
    if is_existing.get('error'):
        return {"error": "User not found"}, 404

    user_id = form.get('user_id')
    user_name = form.get('user_name')
    profile = form.get('profile')

    user = User.query.get(user_id)
    user.user_name = user_name
    user.profile = profile
    db.session.commit()

    return {
               "message": "User updated",
               "user": get_user_by_id(user_id)
           }, 200


@app.post('/user/delete')
def delete_user():
    form = request.get_json()
    if not form.get('user_id'):
        return {"error": "User ID is required"}, 400
    is_existing = get_user_by_id(form.get('user_id'))
    if is_existing.get('error'):
        return {"error": "User not found"}, 404
    
    user_id = form.get('user_id')
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return {
               "message": "User deleted",
           }, 200


def get_user_by_id(user_id: int) -> dict:
    sql = text("""SELECT * FROM  user WHERE  id = :user_id""")
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    if result:
        return dict(result._mapping)
    return {
        "error": "User not found"
    }
