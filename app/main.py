from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category, Product
from app.schemas import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse

app = FastAPI()


@app.get("/message")
def give_statement():
    return {
        "message": "E-commerce API is running"
    }
@app.post("/create", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    new_category = Category(name=category.name)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
@app.get("/get_category", response_model=list[CategoryResponse])
def get_category(
    db: Session = Depends(get_db)
):
    categories = db.query(Category).all()
    return categories

@app.put("/update/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category.name = category_data.name
    db.commit()
    db.refresh(category)
    return category
@app.delete("/delete/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    db.delete(category)
    db.commit()
    return {
        "message": "Category deleted successfully"
    }
from fastapi import HTTPException


@app.post("/products", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == product_data.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category_id=product_data.category_id,
        is_active=product_data.is_active
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
@app.get("/products", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()

    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    category = db.query(Category).filter(
        Category.id == product_data.category_id
    ).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.stock = product_data.stock
    product.category_id = product_data.category_id
    product.is_active = product_data.is_active
    db.commit()
    db.refresh(product)

    return product
@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    db.delete(product)
    db.commit()
    return {
        "message": "Product deleted successfully"
    }

from app.schemas import UserResponse
@app.post("/register",response_model=UserResponse)
def register_user(user_data:UserCreate,
                  db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) |
        (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )
    password_hash=hash_pwd(user_data.password)
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
