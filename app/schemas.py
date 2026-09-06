from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str = Field(min_length=5)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category_id: int = Field(gt=0)
    is_active: bool = True


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: float
    stock: int
    category_id: int
    is_active: bool


class CartItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(ge=1)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int


class OrderResponse(BaseModel):
    id: int
    status: str
    total_amount: float


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float