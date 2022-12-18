from sqlalchemy.orm import Session
from Database.session import get_db
import Models.models as models
import Models.schemas as schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from passlib import hash
from jwt import decode, encode
import os

admin_token = OAuth2PasswordBearer(tokenUrl='/api/admin/token')

user_token = OAuth2PasswordBearer(tokenUrl='/api/user/token')

SECRET = "ffd63878d383d7782bb964956a35565801ff3a49928f48652400ce11aeae90a2"


def sort_products(products):
    return sorted(products, key=lambda product: product.id, reverse=True)

# admin


async def get_admin(db: Session):
    data = db.query(models.Admin).all()
    db.close()
    return data


async def get_admin_by_email(db: Session, email: str):
    data = db.query(models.Admin).filter(models.Admin.email == email).first()
    db.close()
    return data


async def authenticate_admin(db: Session, email: str, password: str):
    admin = await get_admin_by_email(db, email)
    if admin:
        if admin.verify_password(password):
            return admin
    raise HTTPException(
        status_code=400, detail="Incorrect username or password")


async def create_admin_token(admin: schemas.Admin):
    payload = {
        "id": admin.id,
        "email": admin.email,
    }
    token = encode(payload, SECRET)
    return dict(access_token=token, token_type="bearer")


async def get_current_admin(db: Session = Depends(get_db), token: str = Depends(admin_token)):
    try:
        payload = decode(token, SECRET, algorithms=["HS256"])
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        admin = await get_admin_by_email(db=db, email=email)
        return admin
    except:
        raise HTTPException(status_code=400, detail="Invalid token")


async def create_admin(db: Session, admin: schemas.Admin):
    db_admin = models.Admin(email=admin.email, password=hash.bcrypt.hash(
        admin.password), name=admin.name, avatar=admin.avatar)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    db.close()
    return db_admin


async def update_admin(db: Session, email: str, admin_update: schemas.Admin):
    db_admin = db.query(models.Admin).filter(
        models.Admin.email == email).first()
    if db_admin:
        db_admin.email = admin_update.email or db_admin.email
        db_admin.name = admin_update.name or db_admin.name
        db_admin.avatar = admin_update.avatar or db_admin.avatar
        db_admin.password = hash.bcrypt.hash(
            admin_update.password) if admin_update.password else db_admin.password
        db.commit()
        db.refresh(db_admin)
        db.close()
        return db_admin
    else:
        raise HTTPException(status_code=400, detail="Admin not found")


async def delete_admin(db: Session, email: str):
    db_admin = db.query(models.Admin).filter(
        models.Admin.email == email).first()
    if db_admin:
        db.delete(db_admin)
        db.commit()
        db.close()
        return "Delete admin successfully"
    else:
        raise HTTPException(status_code=400, detail="Admin not found")


async def create_product(db: Session, product: schemas.Product, email: str):
    db_product = models.Product(**product.dict(), created_by=email)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product


async def update_product(db: Session, id: int, product_update: schemas.Product, email: str):
    db_product = db.query(models.Product).filter(
        models.Product.id == id).first()
    if db_product:
        db_product.name = product_update.name or db_product.name
        db_product.images = product_update.images or db_product.images
        db_product.size = product_update.size or db_product.size
        db_product.price = product_update.price or db_product.price
        db_product.description = product_update.description or db_product.description
        db_product.quantity = product_update.quantity or db_product.quantity
        db_product.category_id = product_update.category_id or db_product.category_id
        db_product.updated_by = email
        db.commit()
        db.refresh(db_product)
        db.close()
        return db_product
    else:
        raise HTTPException(status_code=400, detail="Product not found")


async def delete_product(db: Session, id: int, email: str):
    db_product = db.query(models.Product).filter(
        models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        db.close()
        return "Delete product successfully by " + email
    else:
        raise HTTPException(status_code=400, detail="Product not found")


async def create_category(db: Session, category: schemas.Category, email: str):
    db_category = models.Category(
        name=category.name, image_review=category.image_review, created_by=email)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    db.close()
    return db_category


async def update_category(db: Session, id: int, category_update: schemas.Category, email: str):
    db_category = db.query(models.Category).filter(
        models.Category.id == id).first()
    if db_category:
        db_category.name = category_update.name or db_category.name
        db_category.image_review = category_update.image_review or db_category.image_review
        db_category.updated_by = email
        db.commit()
        db.refresh(db_category)
        db.close()
        return db_category
    else:
        raise HTTPException(status_code=400, detail="Category not found")


async def delete_category(db: Session, id: int):
    # delete product in category
    db_product = db.query(models.Product).filter(
        models.Product.category_id == id).all()
    if db_product:
        for product in db_product:
            db.delete(product)
            db.commit()
            db.refresh(product)
            db.close()
    # delete category
    db_category = db.query(models.Category).filter(
        models.Category.id == id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        db.close()
        return "Delete category successfully"
    else:
        raise HTTPException(status_code=400, detail="Category not found")


# user

async def get_all_users(db: Session, email: str):
    if email:
        return db.query(models.User).all()
    else:
        raise HTTPException(status_code=400, detail="Admin not found")

async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


async def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


async def create_user(db: Session, user: schemas.User):
    db_user = models.User(email=user.email, password=hash.bcrypt.hash(
        user.password), name=user.name, avatar=user.avatar, phone=user.phone, address=user.address)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


async def create_user_token(user: schemas.User):
    payload = {
        "id": user.id,
        "email": user.email,
    }
    token = encode(payload, SECRET)
    return dict(access_token=token, token_type="bearer")


async def authenticate_user(db: Session, email: str, password: str):
    db_user = db.query(models.User).filter(
        models.User.email == email).first()
    if db_user:
        if hash.bcrypt.verify(password, db_user.password):
            return db_user
        else:
            raise HTTPException(
                status_code=400, detail="Password is incorrect")
    else:
        raise HTTPException(status_code=400, detail="User not found")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(user_token)):
    try:
        payload = decode(token, SECRET, algorithms=["HS256"])
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        user = await get_user_by_email(db=db, email=email)
        return user
    except:
        raise HTTPException(status_code=400, detail="Invalid token")


async def update_user(db: Session, user_update: schemas.User, email: str):
    db_user = db.query(models.User).filter(
        models.User.email == email).first()
    if db_user:
        db_user.email = user_update.email or db_user.email
        db_user.password = hash.bcrypt.hash(
            user_update.password) if user_update.password else db_user.password
        db_user.name = user_update.name or db_user.name
        db_user.avatar = user_update.avatar or db_user.avatar
        db_user.phone = user_update.phone or db_user.phone
        db_user.address = user_update.address or db_user.address
        db.commit()
        db.refresh(db_user)
        db.close()
        return db_user
    else:
        raise HTTPException(status_code=400, detail="User not found")

# cart


async def get_cart_by_user(db: Session, user_id: int):
    data = db.query(models.Cart, models.Product).filter(
        models.Cart.user_id == user_id).filter(models.Cart.product_id == models.Product.id).all()

    if data:
        carts = []
        for cart in data:
            carts.append({
                "id": cart.Cart.id,
                "user_id": cart.Cart.user_id,
                "quantity": cart.Cart.quantity,
                "size": cart.Cart.product_size,
                "product": {
                    "id": cart.Product.id,
                    "name": cart.Product.name,
                    "price": cart.Product.price,
                    "images": cart.Product.images,
                    "category_id": cart.Product.category_id,
                }
            })
        return carts
    else:
        return []


async def create_cart(db: Session, cart: schemas.Cart, user_id: int):
    db_cart = db.query(models.Cart).filter(
        (models.Cart.user_id == user_id) & (models.Cart.product_id == cart.product_id) & (models.Cart.product_size == cart.product_size)).first()

    if db_cart:
        db_cart.quantity = db_cart.quantity + cart.quantity
    else:
        db_cart = models.Cart(
            user_id=user_id, product_id=cart.product_id, quantity=cart.quantity, product_size=cart.product_size)
        db.add(db_cart)

    db.commit()
    db.refresh(db_cart)
    db.close()
    return db_cart


async def update_cart(db: Session, id: int, cart_update: schemas.Cart, user_id: int):
    if user_id:
        db_cart = db.query(models.Cart).filter(
            models.Cart.id == id).first()
        if db_cart:
            db_cart.quantity = cart_update.quantity or db_cart.quantity
            db_cart.product_size = cart_update.product_size or db_cart.product_size
            db.commit()
            db.refresh(db_cart)
            db.close()
            return "Update cart successfully"
        else:
            raise HTTPException(status_code=400, detail="Cart not found")
    else:
        raise HTTPException(status_code=400, detail="User not found")


async def delete_cart(db: Session, id: int, user_id: int):
    if user_id:
        db_cart = db.query(models.Cart).filter(
            models.Cart.id == id).first()
        if db_cart:
            db.delete(db_cart)
            db.commit()
            db.close()
            return "Delete cart successfully"
        else:
            raise HTTPException(status_code=400, detail="Cart not found")
    else:
        raise HTTPException(status_code=400, detail="User not found")

# order


async def get_all_orders(db: Session, email: str):
    if email:
        return db.query(models.Order).all()
    else:
        raise HTTPException(status_code=400, detail="User not found")


async def get_orders_by_user(db: Session, user_id: int):
    data_order_status = db.query(models.Order, models.Status).filter(
        models.Order.user_id == user_id).filter(models.Order.status == models.Status.id).all()

    data_order_status_filter = []
    for data in data_order_status:
        data_order_status_filter.append({
            "id": data.Order.id,
            "user_id": data.Order.user_id,
            "name": data.Order.name,
            "phone": data.Order.phone,
            "address": data.Order.address,
            "email": data.Order.email,
            "note": data.Order.note,
            "total_price": data.Order.total_price,
            "products": data.Order.products,
            "payment_id": data.Order.payment_id,
            "status": data.Status.name,
            "created_at": data.Order.created_at,
            "updated_at": data.Order.updated_at,
        })

    return data_order_status_filter


async def create_order(db: Session, order: schemas.Order, user_id: int):
    db_order = models.Order(user_id=user_id, name=order.name, email=order.email, products=order.products, total_price=order.total_price,
                            address=order.address, phone=order.phone, note=order.note, status=order.status, payment_id=order.payment_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    db.close()

    # delete cart
    db.query(models.Cart).filter(models.Cart.user_id == user_id).delete()
    db.commit()
    db.close()

    return db_order


async def update_order(db: Session, id: int, order_update: schemas.Order, user_id: int):
    if user_id:
        db_order = db.query(models.Order).filter(
            models.Order.id == id).first()
        if db_order:
            db_order.status = order_update.status or db_order.status
            db.commit()
            db.refresh(db_order)
            db.close()
            return db_order
        else:
            raise HTTPException(status_code=400, detail="Order not found")
    else:
        raise HTTPException(status_code=400, detail="User not found")


async def delete_order(db: Session, id: int, user_id: int):
    if user_id:
        db_order = db.query(models.Order).filter(
            models.Order.id == id).first()
        if db_order:
            db.delete(db_order)
            db.commit()
            db.close()
            return "Delete order successfully"
        else:
            raise HTTPException(status_code=400, detail="Order not found")
    else:
        raise HTTPException(status_code=400, detail="User not found")
# No Token


async def get_products(db: Session):
    data = db.query(models.Product).all()
    db.close()
    return sort_products(data)


async def get_product(db: Session, id: int):
    data = db.query(models.Product).filter(models.Product.id == id).first()
    db.close()
    return data


async def get_categories(db: Session):
    data = db.query(models.Category).all()
    db.close()
    return data
