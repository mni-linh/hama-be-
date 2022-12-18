from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import starlette.responses as _responses


import Models.crud as crud
import Models.schemas as schemas

from Database.session import get_db


app = FastAPI()

origins = [
    "http://localhost:3000",
    "vercel.app",
    # "http://localhost:3000",
    # "localhost:3000",
    # "http://localhost:3030",
    # "localhost:3030"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Dependency


@app.get("/", tags=["Root"])
async def root():
    return _responses.RedirectResponse("/redoc")

# Admin


@app.post('/api/admin', tags=["Admin"])
async def create_admin(admin: schemas.Admin, db: Session = Depends(get_db)):
    email = await crud.get_admin_by_email(db, admin.email)
    if email:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        print('Email is not registered')
    admin = await crud.create_admin(db, admin)
    return await crud.create_admin_token(admin)


@app.post('/api/admin/token', tags=["Admin"])
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = await crud.authenticate_admin(db, form_data.username, form_data.password)

    if not admin:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return await crud.create_admin_token(admin)


@app.get('/api/admin/me', tags=["Admin"])
async def get_admin_me(admin: schemas.Admin = Depends(crud.get_current_admin)):
    return admin


@app.put('/api/admin/me', tags=["Admin"])
async def update_admin_me(admin: schemas.Admin = Depends(crud.get_current_admin), db: Session = Depends(get_db), admin_update: schemas.Admin = None):
    if admin.email != admin_update.email:
        email = await crud.get_admin_by_email(db, admin_update.email)
        if email:
            raise HTTPException(
                status_code=400, detail="Email already registered")
    admin_new = await crud.update_admin(db, admin.email, admin_update)
    return await crud.create_admin_token(admin_new)


@app.delete('/api/admin/me', tags=["Admin"])
async def delete_admin_me(admin: schemas.Admin = Depends(crud.get_current_admin), db: Session = Depends(get_db)):
    return await crud.delete_admin(db, admin.email)

# User

@app.get('/api/users', tags=["User"])
async def get_users(db: Session = Depends(get_db), admin: schemas.Admin = Depends(crud.get_current_admin)):
    return await crud.get_all_users(db, admin.email)

@app.post('/api/user', tags=["User"])
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    email = await crud.get_user_by_email(db, user.email)
    phone = await crud.get_user_by_phone(db, user.phone)
    if email:
        raise HTTPException(status_code=400, detail="Email already registered")
    elif phone:
        raise HTTPException(status_code=400, detail="Phone already registered")
    else:
        print('Email and Phone is not registered')
        user = await crud.create_user(db, user)
        return await crud.create_user_token(user)


@app.post('/api/user/token', tags=["User"])
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await crud.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return await crud.create_user_token(user)


@app.get('/api/user/me', tags=["User"])
async def get_user_me(user: schemas.User = Depends(crud.get_current_user)):
    return user


@app.put('/api/user/me', tags=["User"])
async def update_user_me(user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(get_db), user_update: schemas.User = None):
    if user.email != user_update.email:
        email = await crud.get_user_by_email(db, user_update.email)
        if email:
            raise HTTPException(
                status_code=400, detail="Email already registered")
    if user.phone != user_update.phone:
        phone = await crud.get_user_by_phone(db, user_update.phone)
        if phone:
            raise HTTPException(
                status_code=400, detail="Phone already registered")
    user_new = await crud.update_user(db, user_update, user.email)
    return await crud.create_user_token(user_new)

# Product


@app.get('/api/products', tags=["Product"])
async def get_products(db: Session = Depends(get_db)):
    return await crud.get_products(db)


@app.get('/api/products/{product_id}', tags=["Product"])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    return await crud.get_product(db, product_id)


@app.post('/api/products', tags=["Product"])
async def create_product(admin: schemas.Admin = Depends(crud.get_current_admin), product: schemas.Product = None, db: Session = Depends(get_db)):
    return await crud.create_product(db, product, admin.email)


@app.put('/api/products/{product_id}', tags=["Product"])
async def update_product(admin: schemas.Admin = Depends(crud.get_current_admin), product_id: int = None, product: schemas.Product = None, db: Session = Depends(get_db)):
    return await crud.update_product(db, product_id, product, admin.email)


@app.delete('/api/products/{product_id}', tags=["Product"])
async def delete_product(admin: schemas.Admin = Depends(crud.get_current_admin), product_id: int = None, db: Session = Depends(get_db)):
    return await crud.delete_product(db, product_id, admin.email)

# Category


@app.get('/api/categories', tags=["Category"])
async def get_categories(db: Session = Depends(get_db)):
    return await crud.get_categories(db)


@app.post('/api/categories', tags=["Category"])
async def create_category(admin: schemas.Admin = Depends(crud.get_current_admin), category: schemas.Category = None, db: Session = Depends(get_db)):
    return await crud.create_category(db, category, admin.email)


@app.put('/api/categories/{category_id}', tags=["Category"])
async def update_category(admin: schemas.Admin = Depends(crud.get_current_admin), category_id: int = None, category: schemas.Category = None, db: Session = Depends(get_db)):
    return await crud.update_category(db, category_id, category, admin.email)


@app.delete('/api/categories/{category_id}', tags=["Category"])
async def delete_category(admin: schemas.Admin = Depends(crud.get_current_admin), category_id: int = None, db: Session = Depends(get_db)):
    return await crud.delete_category(db, category_id, admin.email)


# cart
@app.get('/api/cart', tags=["Cart"])
async def get_cart(user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    return await crud.get_cart_by_user(db, user.id)


@app.post('/api/cart', tags=["Cart"])
async def create_cart(user: schemas.User = Depends(crud.get_current_user), cart: schemas.Cart = None, db: Session = Depends(get_db)):
    return await crud.create_cart(db, cart, user.id)


@app.put('/api/cart/{cart_id}', tags=["Cart"])
async def update_cart(user: schemas.User = Depends(crud.get_current_user), cart_id: int = None, cart: schemas.Cart = None, db: Session = Depends(get_db)):
    return await crud.update_cart(db, cart_id, cart, user.id)


@app.delete('/api/cart/{cart_id}', tags=["Cart"])
async def delete_cart(user: schemas.User = Depends(crud.get_current_user), cart_id: int = None, db: Session = Depends(get_db)):
    return await crud.delete_cart(db, cart_id, user.id)

# order


@app.get('/api/orders', tags=["Order"])
async def get_all_orders(admin: schemas.Admin = Depends(crud.get_current_admin), db: Session = Depends(get_db)):
    return await crud.get_all_orders(db, admin.email)


@app.get('/api/order', tags=["Order"])
async def get_orders(user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    return await crud.get_orders_by_user(db, user.id)


@app.post('/api/order', tags=["Order"])
async def create_order(user: schemas.User = Depends(crud.get_current_user), order: schemas.Order = None, db: Session = Depends(get_db)):
    return await crud.create_order(db, order, user.id)

@app.put('/api/order/{order_id}', tags=["Order"])
async def update_order(user: schemas.User = Depends(crud.get_current_user), order_id: int = None, order: schemas.Order = None, db: Session = Depends(get_db)):
    return await crud.update_order(db, order_id, order, user.id)

@app.delete('/api/order/{order_id}', tags=["Order"])
async def delete_order(user: schemas.User = Depends(crud.get_current_user), order_id: int = None, db: Session = Depends(get_db)):
    return await crud.delete_order(db, order_id, user.id)