import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import uuid
from faker import Faker

fake = Faker()

class ShopifyOrderGenerator:
    def __init__(self):
        self.products = [
            # Electronics
            {"id": 632910392, "title": "iPhone 14 Pro", "variants": [
                {"id": 39072856, "title": "128GB - Space Black", "sku": "IP14P-128-BLK"},
                {"id": 49148385, "title": "256GB - Space Black", "sku": "IP14P-256-BLK"},
                {"id": 457924702, "title": "512GB - Space Black", "sku": "IP14P-512-BLK"}
            ]},
            {"id": 632910393, "title": "MacBook Pro 16", "variants": [
                {"id": 39072857, "title": "M2 Pro - 16GB - 512GB", "sku": "MBP16-M2-16-512"},
                {"id": 49148386, "title": "M2 Pro - 32GB - 1TB", "sku": "MBP16-M2-32-1TB"},
                {"id": 457924703, "title": "M2 Max - 64GB - 2TB", "sku": "MBP16-M2-64-2TB"}
            ]},
            {"id": 632910394, "title": "iPad Air", "variants": [
                {"id": 39072858, "title": "64GB - Space Gray", "sku": "IPAD-AIR-64-GRAY"},
                {"id": 49148387, "title": "256GB - Space Gray", "sku": "IPAD-AIR-256-GRAY"}
            ]},
            
            # Clothing
            {"id": 632910395, "title": "Classic Fit T-Shirt", "variants": [
                {"id": 39072859, "title": "Small - Black", "sku": "TS-S-BLK"},
                {"id": 49148388, "title": "Medium - Black", "sku": "TS-M-BLK"},
                {"id": 457924704, "title": "Large - Black", "sku": "TS-L-BLK"}
            ]},
            {"id": 632910396, "title": "Slim Fit Jeans", "variants": [
                {"id": 39072860, "title": "30x30 - Blue", "sku": "JN-30-30-BLU"},
                {"id": 49148389, "title": "32x30 - Blue", "sku": "JN-32-30-BLU"},
                {"id": 457924705, "title": "34x30 - Blue", "sku": "JN-34-30-BLU"}
            ]},
            
            # Home & Kitchen
            {"id": 632910397, "title": "Smart Coffee Maker", "variants": [
                {"id": 39072861, "title": "Black", "sku": "CM-BLK"},
                {"id": 49148390, "title": "Silver", "sku": "CM-SLV"}
            ]},
            {"id": 632910398, "title": "Air Purifier", "variants": [
                {"id": 39072862, "title": "White", "sku": "AP-WHT"},
                {"id": 49148391, "title": "Black", "sku": "AP-BLK"}
            ]},
            
            # Beauty & Personal Care
            {"id": 632910399, "title": "Premium Skincare Set", "variants": [
                {"id": 39072863, "title": "Normal Skin", "sku": "SK-NORM"},
                {"id": 49148392, "title": "Dry Skin", "sku": "SK-DRY"},
                {"id": 457924706, "title": "Oily Skin", "sku": "SK-OILY"}
            ]},
            
            # Sports & Outdoors
            {"id": 632910400, "title": "Yoga Mat", "variants": [
                {"id": 39072864, "title": "Purple", "sku": "YM-PUR"},
                {"id": 49148393, "title": "Blue", "sku": "YM-BLU"}
            ]},
            
            # Books
            {"id": 632910401, "title": "Bestselling Novel", "variants": [
                {"id": 39072865, "title": "Hardcover", "sku": "BK-HC"},
                {"id": 49148394, "title": "Paperback", "sku": "BK-PB"}
            ]},
            
            # Toys & Games
            {"id": 632910402, "title": "Board Game Collection", "variants": [
                {"id": 39072866, "title": "Classic Edition", "sku": "BG-CL"},
                {"id": 49148395, "title": "Deluxe Edition", "sku": "BG-DX"}
            ]},
            
            # Additional Electronics
            {"id": 632910403, "title": "Wireless Earbuds", "variants": [
                {"id": 39072867, "title": "Black", "sku": "EB-BLK"},
                {"id": 49148396, "title": "White", "sku": "EB-WHT"}
            ]},
            {"id": 632910404, "title": "Smart Watch", "variants": [
                {"id": 39072868, "title": "42mm - Black", "sku": "SW-42-BLK"},
                {"id": 49148397, "title": "46mm - Black", "sku": "SW-46-BLK"}
            ]},
            
            # Additional Clothing
            {"id": 632910405, "title": "Winter Jacket", "variants": [
                {"id": 39072869, "title": "Small - Navy", "sku": "WJ-S-NAV"},
                {"id": 49148398, "title": "Medium - Navy", "sku": "WJ-M-NAV"},
                {"id": 457924707, "title": "Large - Navy", "sku": "WJ-L-NAV"}
            ]},
            
            # Additional Home & Kitchen
            {"id": 632910406, "title": "Smart Light Bulb Set", "variants": [
                {"id": 39072870, "title": "4-Pack", "sku": "LB-4PK"},
                {"id": 49148399, "title": "8-Pack", "sku": "LB-8PK"}
            ]},
            
            # Additional Beauty Products
            {"id": 632910407, "title": "Luxury Perfume", "variants": [
                {"id": 39072871, "title": "30ml", "sku": "PF-30"},
                {"id": 49148400, "title": "50ml", "sku": "PF-50"}
            ]},
            
            # Additional Sports Equipment
            {"id": 632910408, "title": "Fitness Tracker", "variants": [
                {"id": 39072872, "title": "Black", "sku": "FT-BLK"},
                {"id": 49148401, "title": "Blue", "sku": "FT-BLU"}
            ]},
            
            # Additional Books
            {"id": 632910409, "title": "Cookbook Collection", "variants": [
                {"id": 39072873, "title": "Volume 1", "sku": "CB-V1"},
                {"id": 49148402, "title": "Volume 2", "sku": "CB-V2"}
            ]},
            
            # Additional Toys
            {"id": 632910410, "title": "Educational Toy Set", "variants": [
                {"id": 39072874, "title": "Ages 3-5", "sku": "ET-3-5"},
                {"id": 49148403, "title": "Ages 6-8", "sku": "ET-6-8"}
            ]},
            
            # Additional Electronics
            {"id": 632910411, "title": "Bluetooth Speaker", "variants": [
                {"id": 39072875, "title": "Black", "sku": "BS-BLK"},
                {"id": 49148404, "title": "Red", "sku": "BS-RED"}
            ]},
            
            # Additional Clothing
            {"id": 632910412, "title": "Running Shoes", "variants": [
                {"id": 39072876, "title": "Size 7 - Black", "sku": "RS-7-BLK"},
                {"id": 49148405, "title": "Size 8 - Black", "sku": "RS-8-BLK"},
                {"id": 457924708, "title": "Size 9 - Black", "sku": "RS-9-BLK"}
            ]},
            
            # Additional Home Products
            {"id": 632910413, "title": "Smart Thermostat", "variants": [
                {"id": 39072877, "title": "White", "sku": "ST-WHT"},
                {"id": 49148406, "title": "Black", "sku": "ST-BLK"}
            ]},
            
            # Additional Beauty Products
            {"id": 632910414, "title": "Makeup Brush Set", "variants": [
                {"id": 39072878, "title": "Basic Set", "sku": "MB-BASIC"},
                {"id": 49148407, "title": "Professional Set", "sku": "MB-PRO"}
            ]},
            
            # Additional Sports Equipment
            {"id": 632910415, "title": "Resistance Band Set", "variants": [
                {"id": 39072879, "title": "Light", "sku": "RB-LIGHT"},
                {"id": 49148408, "title": "Medium", "sku": "RB-MED"},
                {"id": 457924709, "title": "Heavy", "sku": "RB-HEAVY"}
            ]},
            
            # Additional Books
            {"id": 632910416, "title": "Self-Help Book", "variants": [
                {"id": 39072880, "title": "Hardcover", "sku": "SH-HC"},
                {"id": 49148409, "title": "Paperback", "sku": "SH-PB"}
            ]},
            
            # Additional Toys
            {"id": 632910417, "title": "Building Blocks Set", "variants": [
                {"id": 39072881, "title": "100 Pieces", "sku": "BB-100"},
                {"id": 49148410, "title": "200 Pieces", "sku": "BB-200"}
            ]},
            
            # Additional Electronics
            {"id": 632910418, "title": "Wireless Charger", "variants": [
                {"id": 39072882, "title": "Black", "sku": "WC-BLK"},
                {"id": 49148411, "title": "White", "sku": "WC-WHT"}
            ]},
            
            # Additional Clothing
            {"id": 632910419, "title": "Dress Shirt", "variants": [
                {"id": 39072883, "title": "Small - White", "sku": "DS-S-WHT"},
                {"id": 49148412, "title": "Medium - White", "sku": "DS-M-WHT"},
                {"id": 457924710, "title": "Large - White", "sku": "DS-L-WHT"}
            ]},
            
            # Additional Home Products
            {"id": 632910420, "title": "Smart Doorbell", "variants": [
                {"id": 39072884, "title": "Black", "sku": "SD-BLK"},
                {"id": 49148413, "title": "Silver", "sku": "SD-SLV"}
            ]},
            
            # Additional Beauty Products
            {"id": 632910421, "title": "Hair Care Kit", "variants": [
                {"id": 39072885, "title": "Normal Hair", "sku": "HC-NORM"},
                {"id": 49148414, "title": "Dry Hair", "sku": "HC-DRY"}
            ]},
            
            # Additional Sports Equipment
            {"id": 632910422, "title": "Jump Rope", "variants": [
                {"id": 39072886, "title": "Standard", "sku": "JR-STD"},
                {"id": 49148415, "title": "Weighted", "sku": "JR-WGT"}
            ]},
            
            # Additional Books
            {"id": 632910423, "title": "Art Book", "variants": [
                {"id": 39072887, "title": "Hardcover", "sku": "AB-HC"},
                {"id": 49148416, "title": "Paperback", "sku": "AB-PB"}
            ]},
            
            # Additional Toys
            {"id": 632910424, "title": "Science Kit", "variants": [
                {"id": 39072888, "title": "Beginner", "sku": "SK-BEG"},
                {"id": 49148417, "title": "Advanced", "sku": "SK-ADV"}
            ]},
            
            # Additional Electronics
            {"id": 632910425, "title": "Power Bank", "variants": [
                {"id": 39072889, "title": "10000mAh", "sku": "PB-10K"},
                {"id": 49148418, "title": "20000mAh", "sku": "PB-20K"}
            ]},
            
            # Additional Clothing
            {"id": 632910426, "title": "Hooded Sweatshirt", "variants": [
                {"id": 39072890, "title": "Small - Gray", "sku": "HS-S-GRY"},
                {"id": 49148419, "title": "Medium - Gray", "sku": "HS-M-GRY"},
                {"id": 457924711, "title": "Large - Gray", "sku": "HS-L-GRY"}
            ]},
            
            # Additional Home Products
            {"id": 632910427, "title": "Smart Plug", "variants": [
                {"id": 39072891, "title": "Single", "sku": "SP-SINGLE"},
                {"id": 49148420, "title": "4-Pack", "sku": "SP-4PK"}
            ]},
            
            # Additional Beauty Products
            {"id": 632910428, "title": "Nail Polish Set", "variants": [
                {"id": 39072892, "title": "Classic Colors", "sku": "NP-CLASSIC"},
                {"id": 49148421, "title": "Trendy Colors", "sku": "NP-TRENDY"}
            ]},
            
            # Additional Sports Equipment
            {"id": 632910429, "title": "Yoga Block Set", "variants": [
                {"id": 39072893, "title": "2 Blocks", "sku": "YB-2"},
                {"id": 49148422, "title": "4 Blocks", "sku": "YB-4"}
            ]},
            
            # Additional Books
            {"id": 632910430, "title": "Photography Guide", "variants": [
                {"id": 39072894, "title": "Digital", "sku": "PG-DIG"},
                {"id": 49148423, "title": "Print", "sku": "PG-PRT"}
            ]},
            
            # Additional Toys
            {"id": 632910431, "title": "Puzzle Set", "variants": [
                {"id": 39072895, "title": "500 Pieces", "sku": "PZ-500"},
                {"id": 49148424, "title": "1000 Pieces", "sku": "PZ-1000"}
            ]},
            
            # Additional Electronics
            {"id": 632910432, "title": "USB-C Hub", "variants": [
                {"id": 39072896, "title": "4-Port", "sku": "UH-4"},
                {"id": 49148425, "title": "7-Port", "sku": "UH-7"}
            ]},
            
            # Additional Clothing
            {"id": 632910433, "title": "Swim Shorts", "variants": [
                {"id": 39072897, "title": "Small - Blue", "sku": "SS-S-BLU"},
                {"id": 49148426, "title": "Medium - Blue", "sku": "SS-M-BLU"},
                {"id": 457924712, "title": "Large - Blue", "sku": "SS-L-BLU"}
            ]},
            
            # Additional Home Products
            {"id": 632910434, "title": "Smart Scale", "variants": [
                {"id": 39072898, "title": "Black", "sku": "SS-BLK"},
                {"id": 49148427, "title": "White", "sku": "SS-WHT"}
            ]},
            
            # Additional Beauty Products
            {"id": 632910435, "title": "Facial Cleanser", "variants": [
                {"id": 39072899, "title": "Normal Skin", "sku": "FC-NORM"},
                {"id": 49148428, "title": "Sensitive Skin", "sku": "FC-SENS"}
            ]},
            
            # Additional Sports Equipment
            {"id": 632910436, "title": "Foam Roller", "variants": [
                {"id": 39072900, "title": "Standard", "sku": "FR-STD"},
                {"id": 49148429, "title": "Extra Firm", "sku": "FR-FIRM"}
            ]},
            
            # Additional Books
            {"id": 632910437, "title": "Language Learning Book", "variants": [
                {"id": 39072901, "title": "Beginner", "sku": "LL-BEG"},
                {"id": 49148430, "title": "Intermediate", "sku": "LL-INT"}
            ]},
            
            # Additional Toys
            {"id": 632910438, "title": "Remote Control Car", "variants": [
                {"id": 39072902, "title": "Basic", "sku": "RC-BASIC"},
                {"id": 49148431, "title": "Advanced", "sku": "RC-ADV"}
            ]},
            
            # Additional Electronics
            {"id": 632910439, "title": "Wireless Mouse", "variants": [
                {"id": 39072903, "title": "Black", "sku": "WM-BLK"},
                {"id": 49148432, "title": "Silver", "sku": "WM-SLV"}
            ]},
            
            # Additional Clothing
            {"id": 632910440, "title": "Formal Dress", "variants": [
                {"id": 39072904, "title": "Small - Black", "sku": "FD-S-BLK"},
                {"id": 49148433, "title": "Medium - Black", "sku": "FD-M-BLK"},
                {"id": 457924713, "title": "Large - Black", "sku": "FD-L-BLK"}
            ]},
            
            # Additional Home Products
            {"id": 632910441, "title": "Smart Lock", "variants": [
                {"id": 39072905, "title": "Black", "sku": "SL-BLK"},
                {"id": 49148434, "title": "Silver", "sku": "SL-SLV"}
            ]}
        ]
        
        self.discount_codes = [
            {"code": "TENOFF", "amount": "10.00", "type": "fixed_amount"},
            {"code": "TWENTYOFF", "amount": "20.00", "type": "fixed_amount"},
            {"code": "PERCENT15", "amount": "15.00", "type": "percentage"},
            {"code": "SUMMER25", "amount": "25.00", "type": "percentage"},
            {"code": "WELCOME10", "amount": "10.00", "type": "percentage"},
            {"code": "FLASH30", "amount": "30.00", "type": "percentage"}
        ]
        
        # Customer segments and their characteristics
        self.customer_segments = {
            "high_value": {
                "order_frequency": (3, 8),  # orders per year
                "avg_order_value": (300, 1000),
                "retention_rate": 0.8,  # 80% chance of returning
                "discount_usage": 0.3  # 30% chance of using discount
            },
            "medium_value": {
                "order_frequency": (2, 5),
                "avg_order_value": (100, 300),
                "retention_rate": 0.6,
                "discount_usage": 0.5
            },
            "low_value": {
                "order_frequency": (1, 3),
                "avg_order_value": (50, 100),
                "retention_rate": 0.4,
                "discount_usage": 0.7
            }
        }
        
        # Initialize customer pool
        self.customer_pool = []
        self.customer_orders = {}  # Track orders per customer

    def _generate_customer_pool(self, num_customers: int):
        """Generate a pool of customers with different segments"""
        self.customer_pool = []
        for _ in range(num_customers):
            customer = self._generate_customer()
            # Assign customer segment
            segment = random.choices(
                list(self.customer_segments.keys()),
                weights=[0.2, 0.5, 0.3]  # 20% high value, 50% medium value, 30% low value
            )[0]
            customer["segment"] = segment
            self.customer_pool.append(customer)
            self.customer_orders[customer["id"]] = []

    def _generate_customer(self) -> Dict[str, Any]:
        """Generate a random customer"""
        first_name = fake.first_name()
        last_name = fake.last_name()
        created_at = fake.date_time_between(start_date="-1y", end_date="now")
        return {
            "id": random.randint(100000000, 999999999),
            "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "created_at": created_at.isoformat(),
            "updated_at": created_at.isoformat(),
            "first_name": first_name,
            "last_name": last_name,
            "state": "enabled",
            "verified_email": True,
            "tax_exempt": False,
            "phone": fake.phone_number(),
            "tags": "",
            "currency": "USD"
        }

    def _generate_address(self) -> Dict[str, Any]:
        """Generate a random address"""
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "address1": fake.street_address(),
            "address2": random.choice(["", fake.secondary_address()]),
            "city": fake.city(),
            "province": fake.state(),
            "country": "United States",
            "zip": fake.zipcode(),
            "phone": fake.phone_number(),
            "company": random.choice([None, fake.company()]),
            "latitude": float(fake.latitude()),
            "longitude": float(fake.longitude()),
            "name": fake.name(),
            "country_code": "US",
            "province_code": fake.state_abbr()
        }

    def _generate_line_item(self, order_id: int, customer_segment: str) -> Dict[str, Any]:
        """Generate a random line item based on customer segment"""
        product = random.choice(self.products)
        variant = random.choice(product["variants"])
        quantity = random.randint(1, 3)
        
        # Adjust price based on customer segment
        segment_config = self.customer_segments[customer_segment]
        min_price, max_price = segment_config["avg_order_value"]
        price = random.uniform(min_price, max_price)
        
        # Adjust discount based on customer segment
        if random.random() < segment_config["discount_usage"]:
            total_discount = round(price * quantity * random.uniform(0.1, 0.3), 2)
        else:
            total_discount = 0
        
        # Calculate tax for the line item
        taxable_amount = (price * quantity) - total_discount
        tax_amount = round(taxable_amount * 0.06, 2)  # 6% tax rate
        
        return {
            "id": random.randint(100000000, 999999999),
            "order_id": order_id,
            "name": f"{product['title']} - {variant['title']}",
            "price": str(round(price, 2)),
            "quantity": quantity,
            "sku": variant["sku"],
            "title": product["title"],
            "variant_id": variant["id"],
            "product_id": product["id"],
            "total_discount": str(total_discount),
            "tax_lines": [
                {
                    "price": str(tax_amount),
                    "rate": 0.06,
                    "title": "State Tax",
                    "price_set": {
                        "shop_money": {
                            "amount": str(tax_amount),
                            "currency_code": "USD"
                        },
                        "presentment_money": {
                            "amount": str(tax_amount),
                            "currency_code": "USD"
                        }
                    }
                }
            ]
        }

    def _generate_order(self, customer: Dict[str, Any], order_date: datetime) -> Dict[str, Any]:
        """Generate an order for a specific customer"""
        order_id = random.randint(100000000, 999999999)
        num_items = random.randint(1, 5)
        
        line_items = [self._generate_line_item(order_id, customer["segment"]) for _ in range(num_items)]
        total_price = sum(float(item["price"]) * item["quantity"] for item in line_items)
        total_discount = sum(float(item["total_discount"]) for item in line_items)
        total_tax = round(total_price * 0.06, 2)  # 6% tax rate
        
        # Generate shipping line
        shipping_line = {
            "id": random.randint(100000000, 999999999),
            "title": random.choice(["Standard Shipping", "Express Shipping", "Free Shipping"]),
            "price": "0.00",
            "code": "Standard",
            "source": "shopify",
            "carrier_identifier": None,
            "requested_fulfillment_service_id": None,
            "discount_allocations": [],
            "tax_lines": []
        }
        
        # Generate tax line
        tax_line = {
            "price": str(total_tax),
            "rate": 0.06,
            "title": "State Tax",
            "price_set": {
                "shop_money": {
                    "amount": str(total_tax),
                    "currency_code": "USD"
                },
                "presentment_money": {
                    "amount": str(total_tax),
                    "currency_code": "USD"
                }
            }
        }
        
        # Generate discount code based on customer segment
        if random.random() < self.customer_segments[customer["segment"]]["discount_usage"]:
            discount_code = random.choice(self.discount_codes)
        else:
            discount_code = None
        
        # Determine order status based on customer segment and order history
        num_previous_orders = len(self.customer_orders[customer["id"]])
        if num_previous_orders > 0:
            financial_status = "paid"  # Returning customers are more likely to have paid orders
            fulfillment_status = random.choice(["fulfilled", "partial"])
        else:
            financial_status = random.choice(["paid", "pending"])
            fulfillment_status = random.choice([None, "fulfilled", "unfulfilled"])
        
        order = {
            "id": order_id,
            "name": f"#{random.randint(1000, 9999)}",
            "email": customer["email"],
            "created_at": order_date.isoformat(),
            "updated_at": (order_date + timedelta(days=random.randint(1, 5))).isoformat(),
            "processed_at": order_date.isoformat(),
            "total_price": str(round(total_price - total_discount + total_tax, 2)),
            "subtotal_price": str(round(total_price, 2)),
            "total_tax": str(total_tax),
            "total_discounts": str(total_discount),
            "currency": "USD",
            "financial_status": financial_status,
            "fulfillment_status": fulfillment_status,
            "customer_id": customer["id"],
            "customer_email": customer["email"],
            "customer_first_name": customer["first_name"],
            "customer_last_name": customer["last_name"],
            "customer_phone": customer["phone"],
            "billing_address": self._generate_address(),
            "shipping_address": self._generate_address(),
            "note": random.choice([None, fake.text(max_nb_chars=200)]),
            "tags": "Returning Customer" if num_previous_orders > 0 else "New Customer",
            "line_items": line_items,
            "customer": customer,
            "shipping_lines": [shipping_line],
            "tax_lines": [tax_line],
            "discount_codes": [discount_code] if discount_code else []
        }
        
        # Track this order for the customer
        self.customer_orders[customer["id"]].append(order)
        return order

    def generate_orders(self, num_orders: int) -> List[Dict[str, Any]]:
        """Generate a list of orders with realistic customer retention patterns"""
        # First, generate a pool of customers
        num_customers = int(num_orders * 0.4)  # 40% of orders will be from returning customers
        self._generate_customer_pool(num_customers)
        
        orders = []
        start_date = datetime.now() - timedelta(days=365)  # Generate orders over the last year
        
        # Generate orders for each customer based on their segment
        for customer in self.customer_pool:
            segment_config = self.customer_segments[customer["segment"]]
            min_orders, max_orders = segment_config["order_frequency"]
            num_customer_orders = random.randint(min_orders, max_orders)
            
            # Generate orders for this customer
            for i in range(num_customer_orders):
                # Space out orders over the year
                order_date = start_date + timedelta(
                    days=random.randint(0, 365),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                order = self._generate_order(customer, order_date)
                orders.append(order)
        
        # Sort orders by creation date
        orders.sort(key=lambda x: x["created_at"])
        return orders

    def save_to_json(self, orders: List[Dict[str, Any]], filepath: str) -> None:
        """Save generated orders to a JSON file"""
        with open(filepath, 'w') as f:
            json.dump({"orders": orders}, f, indent=2)

def main():
    """Example usage of the order generator"""
    generator = ShopifyOrderGenerator()
    orders = generator.generate_orders(1000)  # Generate 1000 orders
    generator.save_to_json(orders, "data/generated_orders.json")

if __name__ == "__main__":
    main() 