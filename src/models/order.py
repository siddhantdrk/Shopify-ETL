from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Money(BaseModel):
    amount: str
    currency_code: str

class MoneySet(BaseModel):
    shop_money: Money
    presentment_money: Money

class Customer(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class Address(BaseModel):
    first_name: str
    last_name: str
    address1: str
    address2: Optional[str] = None
    city: str
    province: str
    country: str
    zip: str
    phone: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class LineItem(BaseModel):
    id: int
    name: str
    price: str
    quantity: int
    sku: str
    title: str
    variant_id: int
    product_id: int
    total_discount: str
    tax_lines: List[dict]

class Order(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    processed_at: datetime
    total_price: str
    subtotal_price: str
    total_tax: str
    total_discounts: str
    currency: str
    financial_status: str
    fulfillment_status: Optional[str] = None
    customer: Customer
    billing_address: Address
    shipping_address: Address
    line_items: List[LineItem]
    shipping_lines: List[dict]
    tax_lines: List[dict]
    discount_codes: List[dict]
    note: Optional[str] = None
    tags: str = "" 