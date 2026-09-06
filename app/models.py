from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, Boolean, ForeignKey, Text
from datetime import datetime
from decimal import Decimal

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="customer")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    cart:Mapped["Cart"]=relationship(back_populates="user")
    orders:Mapped["Order"]=relationship(back_populates="user")
  

class Category(Base):
    __tablename__ = "categories"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50),unique=True)
    products:Mapped[list["Product"]]=relationship(
            back_populates="category"
        )

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now,onupdate=datetime.now)
    category:Mapped["Category"]=relationship(
            back_populates="products"
        )
    cart_items:Mapped[list["CartItem"]]=relationship(
        back_populates="product"
    )
    orderitems:Mapped[list["OrderItem"]]=relationship(
        back_populates="product"
    )

class Cart(Base):
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now,onupdate=datetime.now)
    user:Mapped["User"]=relationship(back_populates="cart")
    cart_items:Mapped[list["CartItem"]]=relationship(
        back_populates="cart"
    )
    
class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    cart:Mapped["Cart"]=relationship(
        back_populates="cart_items"
    )
    product:Mapped["Product"]=relationship(
        back_populates="cart_items"
    )

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending")
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,onupdate=datetime.now)
    orderitems:Mapped[list["OrderItem"]]=relationship(
        back_populates="order"
    )
    user:Mapped["User"]=relationship(back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(
        default=1)
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )
    order:Mapped["Order"]=relationship(
       back_populates="orderitems"
    )
    product:Mapped["Product"]=relationship(back_populates="orderitems")